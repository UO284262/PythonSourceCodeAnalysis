def a():   
    try:
        raise ValueError(1)
    except* TypeError as e:
        print(f'caught {type(e)} with nested {e.exceptions}')
    except* OSError as e:
        print(f'caught {type(e)} with nested {e.exceptions}')
