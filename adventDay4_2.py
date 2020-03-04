print( len( list( filter(
                lambda x: sorted(x) == list(x) and 
                len([ l for l in x if x.count(l) == 2 ]) > 0,
                [ str(i) for i in range(245318,765747) ]
            )
        )
    )
)

    