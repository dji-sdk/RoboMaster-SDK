//
// Created by charmyoung on 2019/12/11.
//
#ifndef S1_OPUS_DECODER_H
#define S1_OPUS_DECODER_H

#include <stdlib.h>
#include <errno.h>
#include <string>
#include <opus/opus.h>
#include <stdio.h>

#include <pybind11/pybind11.h>
namespace py = pybind11;

class PyOpusDecoder{
 public:
  PyOpusDecoder(int frame_size, int sample_rate, int channels):
  FRAME_SIZE(frame_size),SAMPLE_RATE(sample_rate),CHANNELS(channels)
  {
//    printf("Constructor!\n");
    int err;

    decoder_ = opus_decoder_create(SAMPLE_RATE, CHANNELS, &err);
    if (err<0)
    {
      fprintf(stderr, "failed to create decoder: %s\n", opus_strerror(err));
    }
  }
  ~PyOpusDecoder(){
//    printf("Destructor!\n");
    opus_decoder_destroy(decoder_);
  }
  py::bytes Decode(const py::str & in){

    ssize_t len = PYBIND11_BYTES_SIZE(in.ptr());
    const unsigned char* data_in = (const unsigned char*)(PYBIND11_BYTES_AS_STRING(in.ptr()));

    std::string out="";
    opus_int16 *int16_out = new opus_int16[FRAME_SIZE];

    int frame_size = opus_decode(decoder_, data_in, len, int16_out, FRAME_SIZE, 0);
    if (frame_size < 0){
      return out;
    }

    char *pcm = new char[FRAME_SIZE* sizeof(opus_int16)];
    for (int i = 0; i < frame_size; ++i)
    {
      pcm[i * 2] = int16_out[i] & 0xFF;
      pcm[i * 2 + 1] = (int16_out[i] >> 8) & 0xFF;
    }
    std::string(pcm, sizeof(opus_int16) * frame_size).swap(out);
//    printf("Decode with input size %d and output size %d\n",len,out.size());

    delete [] int16_out;
    delete [] pcm;
    return py::bytes(out);
  }
 private:
  int FRAME_SIZE = 960;// 48000Hz/(1000ms/20ms))*1Channel
  int SAMPLE_RATE = 48000;
  int CHANNELS = 1;
  OpusDecoder *decoder_;
};

#endif //S1_OPUS_DECODER_H
