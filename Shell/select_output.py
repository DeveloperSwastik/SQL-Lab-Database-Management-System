def select_output(column_name_list=[], data=()):
    
    if len(data) != 0:
        max_colum_len = [len(str(i)) for i in column_name_list]

        for row in data:

            for index, value in enumerate(row):

                if max_colum_len[index] < len(str(value)):
                    max_colum_len[index] = len(str(value))

        def seprator():
            for index in range(len(column_name_list)):

                if index == 0:
                    print(f'+-{"-"*(max_colum_len[index])}-', end='+')
                elif index == len(column_name_list)-1:
                    print(f'-{"-"*(max_colum_len[index])}-', end='+\n')
                else:
                    print(f'-{"-"*(max_colum_len[index])}-', end='+')

        seprator()

        if len(column_name_list) != 1:

            for index, column_name in enumerate(column_name_list):

                if index == 0:
                    print(
                        f'│ {column_name.capitalize()}',
                        f'''{
                            " "*(
                                abs(
                                    len(str(column_name))-max_colum_len[index]
                                ) + 1
                            )
                        }
                        '''.split('\n')[0], 
                        sep='', 
                        end='│'
                    )
                elif index == len(column_name_list)-1:
                    print(
                        f' {column_name.capitalize()}',
                        f'''{
                            " "*(
                                abs(
                                    len(str(column_name))-max_colum_len[index]
                                ) + 1
                            )
                        }
                        '''.split('\n')[0], 
                        sep='',
                        end='│\n'
                    )
                else:
                    print(
                        f' {column_name.capitalize()}',
                        f'''{
                            " "*(
                                abs(
                                    len(str(column_name))-max_colum_len[index]
                                ) + 1
                            )
                        }
                        '''.split('\n')[0], 
                        sep='',
                        end='│'
                    )

        else:
            print(
                f'\n│ {column_name_list[0].capitalize()}',
                f'''{
                    " "*(
                        abs(
                            len(str(column_name_list[0]))-max_colum_len[index] 
                        ) 
                    )
                }'''.split('\n')[0],
                ' │', 
                sep=''
            )
            
        seprator()

        if len(column_name_list) != 1:

            for row in data:

                for index_1, value in enumerate(row):
                    
                    if index_1 == 0:
                        print(
                            f'│ {str(value).capitalize()}',
                            f'''{
                                " "*abs(
                                    len(str(value))-max_colum_len[index_1]
                                )
                            }''', 
                            end='│'
                        )
                    elif index_1 == len(column_name_list)-1:
                        print(
                            f' {str(value).capitalize()}',
                            f'''{
                                " "*abs(
                                    len(str(value))-max_colum_len[index_1]
                                )
                            }''', 
                            end='│\n'
                        )
                    else:
                        print(
                            f' {str(value).capitalize()}',
                            f'''{
                                " "*abs(
                                    len(str(value))-max_colum_len[index_1]
                                )
                            }''', 
                            end='│'
                        )
            seprator()

            if len(data) > 1:
                print(f'{len(data)} rows in set.')
            else:
                print(f'{len(data)} row in set.')

        else:

            for index,value in enumerate(data):
                
                if index != len(data[0])-1:
                    print(
                            f'│ {str(value[0]).capitalize()}'
                            f'''{
                                " "*abs(len(str(value[0]))-max_colum_len[0])
                            } │'''
                    )                                    
                else:
                    print(
                            f'\n│ {str(value[0]).capitalize()}'
                            f'''{
                                " "*abs(len(str(value[0]))-max_colum_len[0])
                            } │'''
                    )
                    
            seprator()

            if len(data) > 1:
                print(f'\n{len(data)} rows in set.')
            else:
                print(f'\n{len(data)} row in set.')

    else:
        print('\nEmpty set')