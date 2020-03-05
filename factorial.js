let f = n => (( n < 2) ? (n < 0) ? null : 1 :  n * f( n - 1 ))


const Recurse = ( state , condition , operation ) =>
{
    while ( condition(state) ) { state = operation(state) }
    return state ;
}

