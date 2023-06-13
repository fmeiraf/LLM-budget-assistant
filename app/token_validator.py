import tiktoken


class TokenValidator:
    def __init__(self, model: str):
        self.model = model

    def get_token_count(self, input: str):
        enc = tiktoken.encoding_for_model(self.model)
        return len(enc.encode(input))

    def is_valid_count(
        self, base_prompt: str, transaction_input: str, max_tokens_threshold: int = 2000
    ):
        base_prompt_tokens = self.get_token_count(
            base_prompt
        )  # need to add a way to inject the prompt template with transaction_input (might add guardrails obj as class attribute)
        transaction_input_tokens = self.get_token_count(transaction_input)
        final_expected_tokens = (
            (base_prompt_tokens + transaction_input_tokens) * 2
        ) + transaction_input_tokens  # * 2 here because we are adding the prompt and the response
        self.expected_tokens = final_expected_tokens
        return final_expected_tokens <= max_tokens_threshold

    def split_tokens(
        self,
        input: str,
        str_sep: str = "\n",
        split_factor: int = 2,
    ):
        split_input = input.split(str_sep)
        split_divider = len(split_input) // split_factor

        splitted_inputs = [
            str_sep.join(split_input[i : i + split_divider])
            for i in range(0, len(split_input), split_divider)
        ]

        return splitted_inputs

    def validate_input(
        self, inputs: list[str], base_prompt: str, max_tokens_threshold: int = 2000
    ):
        final_inputs = []
        for input in inputs:
            if self.is_valid_count(
                base_prompt=base_prompt,
                transaction_input=input,
                max_tokens_threshold=max_tokens_threshold,
            ):
                final_inputs.append(
                    (input, self.expected_tokens)
                )  # when inputs are invalid the return value will be a list, so just making this standard
            else:
                new_input = self.split_tokens(input=input)
                return self.validate_input(
                    inputs=new_input,
                    base_prompt=base_prompt,
                    max_tokens_threshold=max_tokens_threshold,
                )

        return final_inputs
