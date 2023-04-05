# RUN: %PYTHON %s %config_flag
# UNSUPPORTED: vmvx

import absl.testing
import numpy
import test_util

model_path = "https://tfhub.dev/tensorflow/lite-model/albert_lite_base/squadv1/1?lite-format=tflite"

class AlbertTest(test_util.TFLiteModelTest):
  def __init__(self, *args, **kwargs):
    super(AlbertTest, self).__init__(model_path, *args, **kwargs)

  # Inputs modified to be useful albert inputs.
  def generate_inputs(self, input_details):
    for input in input_details:
      absl.logging.info("\t%s, %s", str(input["shape"]), input["dtype"].__name__)

    args = []
    args.append(numpy.random.randint(low=0, high=256, size=input_details[0]["shape"], dtype=input_details[0]["dtype"]))
    args.append(numpy.ones(shape=input_details[1]["shape"], dtype=input_details[1]["dtype"]))
    args.append(numpy.zeros(shape=input_details[2]["shape"], dtype=input_details[2]["dtype"]))
    return args

  def compare_results(self, iree_results, tflite_results, details):
    super(AlbertTest, self).compare_results(iree_results, tflite_results, details)
    self.assertTrue(numpy.isclose(iree_results[0], tflite_results[0], atol=1e-4).all())
    self.assertTrue(numpy.isclose(iree_results[1], tflite_results[1], atol=1e-4).all())

  def test_compile_tflite(self):
    self.compile_and_execute()

if __name__ == '__main__':
  absl.testing.absltest.main()
