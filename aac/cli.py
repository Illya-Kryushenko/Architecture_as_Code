import argparse
from model import load_model
from validator import check_model_against_terraform_state

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--state", required=True)
    args = parser.parse_args()

    model = load_model(args.model)
    success = check_model_against_terraform_state(model, args.state)
    raise SystemExit(0 if success else 1)
    
if __name__ == "__main__":
    main()
