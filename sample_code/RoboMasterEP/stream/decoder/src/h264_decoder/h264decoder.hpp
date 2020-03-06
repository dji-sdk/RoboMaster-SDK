#ifndef S1_H264_DECODER_H
#define S1_H264_DECODER_H
/*
This h264 decoder class  is just a thin wrapper around libav 
functions to decode h264 videos. It would have been easy to use 
libav directly in   the python module code but I like to keep these 
things separate.
 
It is mostly based on roxlu's code. See
http://roxlu.com/2014/039/decoding-h264-and-yuv420p-playback

However, in contrast to roxlu's code the color space conversion is
done by libav functions - so on the CPU, I suppose.

Most functions/members throw exceptions. This way, error states are 
conveniently forwarded to python via the exception translation 
mechanisms of boost::python.  
*/
extern "C" {
#include <libavcodec/avcodec.h>
#include <libavutil/avutil.h>
#include <libavutil/mem.h>
#include <libswscale/swscale.h>
}
// for ssize_t (signed int type as large as pointer type)
#include <cstdlib>
#include <stdexcept>
#include <utility>

#ifndef PIX_FMT_RGB24
#define PIX_FMT_RGB24 AV_PIX_FMT_RGB24
#endif

#ifndef CODEC_CAP_TRUNCATED
#define CODEC_CAP_TRUNCATED AV_CODEC_CAP_TRUNCATED
#endif

#ifndef CODEC_FLAG_TRUNCATED
#define CODEC_FLAG_TRUNCATED AV_CODEC_FLAG_TRUNCATED
#endif
typedef unsigned char ubyte;

/* For backward compatibility with release 9 or so of libav */
#if (LIBAVCODEC_VERSION_MAJOR <= 54)
#  define av_frame_alloc avcodec_alloc_frame
#  define av_frame_free  avcodec_free_frame
#endif


class H264Exception : public std::runtime_error
{
 public:
  H264Exception(const char* s) : std::runtime_error(s) {}
};

class H264InitFailure : public H264Exception
{
 public:
  H264InitFailure(const char* s) : H264Exception(s) {}
};

class H264DecodeFailure : public H264Exception
{
 public:
  H264DecodeFailure(const char* s) : H264Exception(s) {}
};


class H264Decoder
{
  /* Persistent things here, using RAII for cleanup. */
  AVCodecContext        *context;
  AVFrame               *frame;
  AVCodec               *codec;
  AVCodecParserContext  *parser;
  /* In the documentation example on the github master branch, the 
packet is put on the heap. This is done here to store the pointers 
to the encoded data, which must be kept around  between calls to 
parse- and decode frame. In release 11 it is put on the stack, too. 
  */
  AVPacket              *pkt;
 public:
  H264Decoder()
  {
    avcodec_register_all();

    codec = avcodec_find_decoder(AV_CODEC_ID_H264);
    if (!codec)
      throw H264InitFailure("cannot find decoder");

    context = avcodec_alloc_context3(codec);
    if (!context)
      throw H264InitFailure("cannot allocate context");

    if(codec->capabilities & CODEC_CAP_TRUNCATED) {
      context->flags |= CODEC_FLAG_TRUNCATED;
    }

    int err = avcodec_open2(context, codec, nullptr);
    if (err < 0)
      throw H264InitFailure("cannot open context");

    parser = av_parser_init(AV_CODEC_ID_H264);
    if (!parser)
      throw H264InitFailure("cannot init parser");

    frame = av_frame_alloc();
    if (!frame)
      throw H264InitFailure("cannot allocate frame");

#if 1
    pkt = new AVPacket;
    if (!pkt)
      throw H264InitFailure("cannot allocate packet");
    av_init_packet(pkt);
#endif
  }
  ~H264Decoder(){
    av_parser_close(parser);
    avcodec_close(context);
    av_free(context);
    av_frame_free(&frame);
#if 1
    delete pkt;
#endif
  }
  /* First, parse a continuous data stream, dividing it into 
packets. When there is enough data to form a new frame, decode 
the data and return the frame. parse returns the number 
of consumed bytes of the input stream. It stops consuming 
bytes at frame boundaries.
  */
  ssize_t parse(const unsigned char* in_data, ssize_t in_size)
  {
    auto nread = av_parser_parse2(parser, context, &pkt->data, &pkt->size,
                                  in_data, in_size,
                                  0, 0, AV_NOPTS_VALUE);
    return nread;
  }

  bool is_frame_available() const{
    return pkt->size > 0;
  }
  const AVFrame& decode_frame(){
    int got_picture = 0;
    int nread = avcodec_decode_video2(context, frame, &got_picture, pkt);
    if (nread < 0 || got_picture == 0)
      throw H264DecodeFailure("error decoding frame\n");
    return *frame;
  }
};

// TODO: Rename to OutputStage or so?!
class ConverterRGB24
{
  SwsContext *context;
  AVFrame *framergb;

 public:
  ConverterRGB24(){
    framergb = av_frame_alloc();
    if (!framergb)
      throw H264DecodeFailure("cannot allocate frame");
    context = nullptr;
  }
  ~ConverterRGB24(){
    sws_freeContext(context);
    av_frame_free(&framergb);
  }

  /*  Returns, given a width and height, 
      how many bytes the frame buffer is going to need. */
  int predict_size(int w, int h)
  {
    return avpicture_fill((AVPicture*)framergb, nullptr, PIX_FMT_RGB24, w, h);
  }
  /*  Given a decoded frame, convert it to RGB format and fill 
out_rgb with the result. Returns a AVFrame structure holding 
additional information about the RGB frame, such as the number of
bytes in a row and so on. */
  const AVFrame& convert(const AVFrame &frame, unsigned char* out_rgb){
    int w = frame.width;
    int h = frame.height;
    int pix_fmt = frame.format;

    context = sws_getCachedContext(context,
                                   w, h, (AVPixelFormat)pix_fmt,
                                   w, h, PIX_FMT_RGB24, SWS_BILINEAR,
                                   nullptr, nullptr, nullptr);
    if (!context)
      throw H264DecodeFailure("cannot allocate context");

    // Setup framergb with out_rgb as external buffer. Also say that we want RGB24 output.
    avpicture_fill((AVPicture*)framergb, out_rgb, PIX_FMT_RGB24, w, h);
    // Do the conversion.
    sws_scale(context, frame.data, frame.linesize, 0, h,
              framergb->data, framergb->linesize);
    framergb->width = w;
    framergb->height = h;
    return *framergb;
  }
};

void disable_logging(){
  av_log_set_level(AV_LOG_QUIET);
}

/* Wrappers, so we don't have to include libav headers. */
std::pair<int, int> width_height(const AVFrame& f){
  return std::make_pair(f.width, f.height);
}
int row_size(const AVFrame& f){
  return f.linesize[0];
}

/* all the documentation links
 * My version of libav on ubuntu 16 appears to be from the release/11 branch on github
 * Video decoding example: https://libav.org/documentation/doxygen/release/11/avcodec_8c_source.html#l00455
 * https://libav.org/documentation/doxygen/release/9/group__lavc__decoding.html
 * https://libav.org/documentation/doxygen/release/11/group__lavc__parsing.html
 * https://libav.org/documentation/doxygen/release/9/swscale_8h.html
 * https://libav.org/documentation/doxygen/release/9/group__lavu.html
 * https://libav.org/documentation/doxygen/release/9/group__lavc__picture.html
 * http://dranger.com/ffmpeg/tutorial01.html
 */

#endif //S1_H264_DECODER_H