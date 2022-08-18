def input_query(user, profile):
    query = input(
        f'SQL~Lab~Shell\{(profile).capitalize()}\{user.capitalize()} >>> '
    )
    
    while(
        not query.strip().endswith(';')
    ):
        add_query = input(f'{" "*(len(profile) + len(user) + 15)} >>> ')
        query += f' {add_query}'

    while(
        query.count('  ')
    ):
        query = query.replace('  ',' ')
    
    return query.strip()