from math import *
from random import *

class rabin:
    def __init__(self):
        pass
    def get_big(self, bit):    #get a big number x that x % 4 = 3
        big = 1
        for i in range(bit-3):
            temp = randrange(0,2)
            big = big * 2 + temp
        big = big * 4 + 3
        return big

    def get_prime(self, bit):  #get d-h safe-prime
        b = False
        while b == False:
            b = True
            p = self.get_big(bit-1)-2
            for i in range(10):
                base = randrange(2,1000)
                x = self.mill(p,base)
                if x == 0:
                    b = False
                    break
            p = p*2 + 1
            for i in range(10):
                base = randrange(2,1000)
                x = self.mill(p,base)
                if x == 0:
                    b = False
                    break
        return p

    def powmod(self, b, m, n):
        if m==0:
            return 1
        ans = 1
        tmod = b % n
        while m != 0:
            if m%2 :
               ans=(ans * tmod) % n
            tmod = (tmod * tmod) % n
            m /= 2
        return ans

    def mill(self, n, base):   #rabin_miller test
        m = n - 1
        b,k = base, 0
        while (m % 2) == 0:
            m = m / 2
            k += 1
        t = self.powmod(b, m, n)
        if (t%n) == 1 or (t%n) == n-1:
            return True
        for i in range(k-1):    
            t = pow(t,2)
        if (t%n) == 1:
            return False;
        elif (t%n) == (n-1):
            return True;
        else:
            if (t%n) == 1:
                return True
            elif (t%n) == (n-1):
                return True
        return False

    def euclid(self,a,p):    #calculate s1: (s1*a)%p = 1
        s0,s1,t0,t1 = 1,0,0,1
        r0,r1 = a,p
        if r1:
            q0 = r0 / r1
            r2 = r0 - (q0 * r1)
            r0,r1 = r1,r2
        while r1:
            q1 = r0 / r1
            r2 = r0 - (q1 * r1)
            s2 = s0 - (q0 * s1)
            t2 = t0 - (q0 * t1)
            q0 = q1
            r0,r1 = r1,r2
            s0,s1 = s1,s2
            t0,t1 = t1,t2
        if s1 < 0:
            s1 = s1 + p
        return s1

    def encode(self, m, n):   #get encrypt every 5-bits
         i = 0
         l = len(m)
         cipher = []
         ci = 0
         for i in range(l):
            temp = ord(m[i])
            if (i%5) == 0:
               ci = temp
               if i == (l-1):
                   cipher.append(self.powmod(ci,2,n))
            elif (i%5) == 4:
                ci = ci * 256
                ci = ci + temp
                #print ci
                cipher.append(self.powmod(ci,2,n))
                ci = 0
            else:
                ci = ci * 256
                ci = ci + temp
                if i == (l-1):
                    cipher.append(self.powmod(ci,2,n))
         s=""
         for i in cipher:
             s+=str(i)
             s+=" "
         s= s[0:len(s)-1]
         return s

    def decode(self,s, p, q):
          m=[]
          for i in s.split(" "):
              m.append(long(i))
          l = len(m)
          expressly = ""
          for i in range(l):
             #decode
             temp1 = self.powmod(m[i],(p+1)/4,p)
             temp2 = self.powmod(m[i],(q+1)/4,q)
             u = self.euclid(q,p)
             v = self.euclid(p,q)
             temp1 = (temp1*u*q + temp2*v*p + p*q) % (p*q)
             temp2 = (temp1*u*q - temp2*v*p + p*q) % (p*q)
             temp3 = (-temp1*u*q + temp2*v*p + p*q) % (p*q)
             temp4 = (-temp1*u*q - temp2*v*p + p*q) % (p*q)
             if temp1 < 1099511627776:
                 temp = temp1
             elif temp2 < 1099511627776:
                 temp = temp2
             elif temp3 < 1099511627776:
                 temp = temp3
             elif temp4 < 1099511627776:
                 temp = temp4
             #get decrypt  
             tems = ""
             tem = 0
             while(temp >= 4294967296):
                 temp -= 4294967296
                 tem += 1
             if(tem):
                 tems += chr(tem)
             tem = 0    
             while(temp >= 16777216):
                 temp -= 16777216
                 tem += 1
             if(tem):
                 tems += chr(tem)
             tem = 0
             while(temp >= 65536):
                temp -= 65536
                tem += 1
             if(tem):
                 tems += chr(tem)
             tem = 0
             while(temp >= 256):
                temp -= 256
                tem += 1
             if(tem):
                 tems += chr(tem)
             tems += chr(temp)
             expressly += tems
          return expressly

    def getrabinkey(self):
        b=False
        while b == False:
            b = True
            p = self.get_big(28)
            for i in range(10):
                base = randrange(2,1000)
                x = self.mill(p,base)
                if x == 0:
                    b = False
                    break
        self.p = p
        b=False
        while b == False:
            b = True
            q = self.get_big(28)
            for i in range(10):
                base = randrange(2,1000)
                x = self.mill(q,base)
                if x == 0:
                    b = False
                    break
        self.q = q
        self.n = p * q
        return (self.n, [self.p, self.q])
    
