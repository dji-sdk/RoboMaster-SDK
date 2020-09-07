#include "opus_decoder.h"
#include <pybind11/pybind11.h>
namespace py = pybind11;
PYBIND11_MODULE(opus_decoder, m) {
  m.doc()="opus_decoder for pybind11 plugin";
  py::class_<PyOpusDecoder> ad(m, "opus_decoder");
  ad.def(py::init<int, int, int>(),py::arg("frame_size") = 960,
      py::arg("sample_rate") = 48000, py::arg("channels") = 1);
  ad.def("decode", &PyOpusDecoder::Decode, "Decode Function",py::arg("in"));

}