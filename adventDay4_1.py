print( len( list( filter(
                lambda x: sorted(x) == list(x) and len(set(x)) < len(x), 
                [ str(i) for i in range(245318,765747)]
            )
        )
    )
)




