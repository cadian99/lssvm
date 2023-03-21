from gda import ExponentialDiscreteGDA
from eth_abi import encode_single
import argparse
import math

def main(args): 
    if args.type == "exp_discrete": 
        calculate_exp_discrete(args)
    elif args.type == "calculate_new_spot_price":
        calculate_new_spot_price(args)


def calculate_exp_discrete(args):
    gda = ExponentialDiscreteGDA(args.initial_price / (10 ** 18), args.decay_constant / (10 ** 18), args.scale_factor / (10 ** 18))
    price = gda.get_cumulative_purchase_price(args.num_total_purchases, args.time_since_start, args.quantity)
    ## convert price to wei 
    price *= (10 ** 18)
    enc = encode_single('uint256', int(price))
    ## append 0x for FFI parsing 
    print("0x" + enc.hex())


def calculate_new_spot_price(args):
    k = args.initial_price / (10**18)
    alpha_pow_m_n = math.pow(args.scale_factor / (10 ** 18), args.num_total_purchases + args.quantity)
    decay_factor = math.exp((args.decay_constant / (10 ** 18)) * args.time_since_start)
    new_spot_price = k * alpha_pow_m_n / decay_factor * (10 ** 18)
    enc = encode_single('uint256', int(new_spot_price))
    print("0x" + enc.hex())


def parse_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("type")
    parser.add_argument("--scale_factor", type=int)
    parser.add_argument("--decay_constant", type=int)
    parser.add_argument("--emission_rate", type=int)
    parser.add_argument("--initial_price", type=int)
    parser.add_argument("--num_total_purchases", type=int)
    parser.add_argument("--time_since_start", type=int)
    parser.add_argument("--age_last_auction", type=int)
    parser.add_argument("--quantity", type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args() 
    main(args)