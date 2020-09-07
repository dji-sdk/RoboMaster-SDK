#include <cstdio>
#include <stdexcept>
#include <cassert>
#include <pybind11/pybind11.h>
#include "h264decoder.hpp"

namespace py = pybind11;
using ubyte = unsigned char;

class GILScopedReverseLock
{
  // see https://docs.python.org/2/c-api/init.html (Releasing the GIL ...)  
public:
  GILScopedReverseLock() 
    : state(nullptr)
  {
    unlock();
  }
  
  ~GILScopedReverseLock()
  {
    lock();
  }
  
  void lock() 
  {
    // Allow successive calls to lock. 
    // E.g. lock() followed by destructor.
    if (state != nullptr)
    {
      PyEval_RestoreThread(state);
      state = nullptr;
    }
  }
  
  void unlock()
  {
    assert (state == nullptr);
    state = PyEval_SaveThread();
  }
  
  GILScopedReverseLock(const GILScopedReverseLock &) = delete;
  GILScopedReverseLock(const GILScopedReverseLock &&) = delete;
  GILScopedReverseLock operator=(const GILScopedReverseLock &) = delete;
  GILScopedReverseLock operator=(const GILScopedReverseLock &&) = delete;
private:
  PyThreadState *state;
};

/* The class wrapped in python via boost::python */
class PyH264Decoder
{
 public:
  H264Decoder decoder;
  ConverterRGB24 converter;

  /* Extract frames from input stream. Stops at frame boundaries and returns the number of consumed bytes
   * in num_consumed.
   * 
   * If a frame is completed, is_frame_available is set to true, and the returned python tuple contains
   * formation about the frame as well as the frame buffer memory. 
   * 
   * Else, i.e. all data in the buffer is consumed, is_frame_available is set to false. The returned tuple
   * contains dummy data.
   */
  py::tuple decode_frame_impl(const ubyte *data_in, ssize_t len, ssize_t &num_consumed, bool &is_frame_available)
  {
    GILScopedReverseLock gilguard;
    num_consumed = decoder.parse((ubyte*)data_in, len);

    if (is_frame_available = decoder.is_frame_available())
    {
      const auto &frame = decoder.decode_frame();
      int w, h; std::tie(w,h) = width_height(frame);
      Py_ssize_t out_size = converter.predict_size(w,h);

      gilguard.lock();
      //   Construction of py::handle causes ... TODO: WHAT? No increase of ref count ?!
      py::object py_out_str = py::reinterpret_steal<py::object>(PYBIND11_BYTES_FROM_STRING_AND_SIZE(NULL, out_size));
      char* out_buffer = PYBIND11_BYTES_AS_STRING(py_out_str.ptr());

      gilguard.unlock();
      const auto &rgbframe = converter.convert(frame, (ubyte*)out_buffer);

      gilguard.lock();
      return py::make_tuple(py_out_str, w, h, row_size(rgbframe));
    }
    else
    {
      gilguard.lock();
      return py::make_tuple(py::none(), 0, 0, 0);
    }
  }
public:
//  PyH264Decoder(){}
//  ~PyH264Decoder()= default;
  /* Decoding style analogous to c/c++ way. Stop at frame boundaries. 
   * Return tuple containing frame data as above as nested tuple, and an integer telling how many bytes were consumed.  */
  py::tuple decode_frame(const py::str &data_in_str){
    ssize_t len = PYBIND11_BYTES_SIZE(data_in_str.ptr());
    const ubyte* data_in = (const ubyte*)(PYBIND11_BYTES_AS_STRING(data_in_str.ptr()));

    ssize_t num_consumed = 0;
    bool is_frame_available = false;
    auto frame = decode_frame_impl(data_in, len, num_consumed, is_frame_available);

    return py::make_tuple(frame, num_consumed);
  }
  /* Process all the input data and return a list of all contained frames. */
  py::list  decode(const py::str &data_in_str) {
    ssize_t len = PYBIND11_BYTES_SIZE(data_in_str.ptr());
    const ubyte* data_in = (const ubyte*)(PYBIND11_BYTES_AS_STRING(data_in_str.ptr()));

    py::list out;

    try
    {
      while (len > 0)
      {
        ssize_t num_consumed = 0;
        bool is_frame_available = false;

        try
        {
          auto frame = decode_frame_impl(data_in, len, num_consumed, is_frame_available);
          if (is_frame_available)
          {
            out.append(frame);
          }
        }
        catch (const H264DecodeFailure &e)
        {
          if (num_consumed <= 0)
            // This case is fatal because we cannot continue to move ahead in the stream.
            throw e;
        }

        len -= num_consumed;
        data_in += num_consumed;
      }
    }
    catch (const H264DecodeFailure &e)
    {
    }

    return out;
  }
};



PYBIND11_MODULE(libh264decoder, m)
{
  PyEval_InitThreads(); // need for release of the GIL (http://stackoverflow.com/questions/8009613/boost-python-not-supporting-parallelism)
  py::class_<PyH264Decoder>(m,"H264Decoder").def(py::init<>())
                            .def("decode_frame", &PyH264Decoder::decode_frame)
                            .def("decode", &PyH264Decoder::decode);
  m.def("disable_logging", disable_logging);
}