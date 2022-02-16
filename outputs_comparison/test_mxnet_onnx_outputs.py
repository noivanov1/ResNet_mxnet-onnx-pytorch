import sys
import os
import inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))

import numpy as np
import config
import args_parser

from tools import write_logfile
from prettytable import PrettyTable


def read_embedding_file(embedding_file: str) -> np.ndarray:
    """
    Read embeddings from .npy file.
    """
    return np.load(embedding_file)


def dim_test(vector_1: np.ndarray, vector_2: np.ndarray, vector_3: np.ndarray):
    """
    Test MXNet, ONNX and ONNX Runtime embeddings size compatibility.
    """
    if len(vector_1) == len(vector_2) and len(vector_1) == len(vector_3):
        print('Embeddings size match')
    else:
        raise Exception('Embeddings size do not match, check embeddings and conversion code')


def absolute_error(vector_1: np.ndarray, vector_2: np.ndarray) -> float:
    """
    Calculate absolute errors.
    """
    return np.max(abs(vector_1 - vector_2))


def relative_error(vector_1: np.ndarray, vector_2: np.ndarray) -> float:
    """
    Calculate relative errors.
    First vector is STRONGLY MXNet model embedding.
    """
    errors_list = []
    for i in range(len(vector_1)):
        errors_list.append(abs((vector_1[i] - vector_2[i]) / vector_1[i]))
    return np.max(errors_list)


def create_log(max_abs_onnx: float, max_abs_onnxruntime: float, max_rel_onnx: float, max_rel_onnxruntime: float) -> str:
    """
    Log file containing table of ONNX (MXNet back) and ONNX Runtime embeddings errors.
    """
    headers = ["MAX Errors to original MXNet model ", "Max Absolute error", "Max Relative error"]
    log_table = PrettyTable(headers)
    log_table.add_row(["ONNX (MXNet back) inference", max_abs_onnx, max_rel_onnx])
    log_table.add_row(["ONNX Runtime inference", max_abs_onnxruntime, max_rel_onnxruntime])
    return log_table.get_string()


def main():
    mxnet_embedding = read_embedding_file(config.mxnet_output_file)
    onnx_mxnet_embedding = read_embedding_file(config.onnx_mxnet_output_file)
    onnxruntime_embedding = read_embedding_file(config.onnxruntime_output_file)

    dim_test(mxnet_embedding, onnx_mxnet_embedding, onnxruntime_embedding)

    max_abs_onnx = absolute_error(onnx_mxnet_embedding, mxnet_embedding)
    max_abs_onnxruntime = absolute_error(onnxruntime_embedding, mxnet_embedding)

    max_rel_onnx = relative_error(mxnet_embedding, onnx_mxnet_embedding)
    max_rel_onnxruntime = relative_error(mxnet_embedding, onnxruntime_embedding)

    test_log_table = create_log(max_abs_onnx, max_abs_onnxruntime, max_rel_onnx, max_rel_onnxruntime)
    write_logfile(args_parser.args.test_mx_onnx, test_log_table)

    print(f'Done! Check {args_parser.args.test_mx_onnx}')


if __name__ == "__main__":
    main()