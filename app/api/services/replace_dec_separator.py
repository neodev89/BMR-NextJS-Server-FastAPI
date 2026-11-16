def replace_dec_separator(value: int | float | str | list[int | float | str]) -> str | list[str]:
    if isinstance(value, (list, tuple)):
        return [str(v).replace(".", ",") for v in value]
    
    return str(value).replace(".", ",")