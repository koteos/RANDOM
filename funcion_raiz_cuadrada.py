def cuadrado(x):  
    """Returns the square root of x, if x is a perfect square.  
    Prints an error message and returns None otherwise"""  
    ans = 0  
    if x > 0:  
        while ans*ans < x: ans = ans + 1  
        if ans*ans != x:  
            print (x, 'is not a perfect square')  
            return None  
        else: return ans  
    else:  
        print (x, 'is a negative number')  
        return None


def f(x):  
    x = x + 1  
    return x

##x = 25 
##ans = 0  
##if x > 0:  
##    while ans*ans < x:  
##        ans = ans + 1  
##        print ('ans =', ans)  
##    if ans*ans != x:  
##        print (x, 'is not a perfect square')  
##    else:   
##        print (ans)  
##else:   
##    print (x, 'is a negative number')
