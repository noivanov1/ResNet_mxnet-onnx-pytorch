import mxnet as mx
import args_parser

from tools import load_model_mxnet, preprocess_image, get_model_output_onnx_mxnet, save_output
from ast import literal_eval


def main():
    ctx = mx.cpu()
    image = preprocess_image(args_parser.args.input_image, literal_eval(str(args_parser.args.input_shape)))
    model = load_model_mxnet(ctx, args_parser.args.prefix, args_parser.args.epoch, image)
    model_out = get_model_output_onnx_mxnet(model, image)
    save_output(args_parser.args.mxnet_model_output, model_out)
    print(f'Done! Check {args_parser.args.mxnet_model_output}')


if __name__ == "__main__":
    main()
