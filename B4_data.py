import math

#--------------------------------------------------------------------------------------------------
class Data:

    #----------------------------------------------------------------------------------------------
    # constructor: self is a 'data' object created in B
    def __init__(self, reactor):
        pass

    #----------------------------------------------------------------------------------------------
    # material properties: self is a 'data' object created in B, inp is a dictionary of input data dependent on the material
    def matpro(self, inp):

        # he: helium gas
        if inp['type'] == 'he':
            t = inp['t']
            k = 2.639e-3*t**0.7085
            return {'k':k}

        # mox: mixed uranium-plutonium oxide fuel
        if inp['type'] == 'mox':
            t,b,por,pu,x = inp['t'],inp['b'],inp['por'],inp['pu'],inp['x']
            # density (kg/m3)
            rho = (11460*pu + 10960*(1 - pu)) * (1 - por)
            # specific heat (J/kg-K), D.L. Hagrman, et al., "MATPRO-version 11", TREE-NUREG-1280, Rev 1, Idaho National Engineering Laboratory (1980).
            cp = 15.496*(19.53*539**2 * math.exp(539/t) / (t**2 * (math.exp(539/t) - 1)**2) + 2*9.25e-04*t + 6.02e06*4.01e4 / (1.987*t**2) * math.exp(-4.01e4/(1.987*t)))
            # thermal conductivity (W/m-K), Y. Philipponneau, J. Nuclear Matter., 188 (1992) 194-197
            k = (1/( 1.528*math.sqrt(x+0.00931) - 0.1055 + 0.44*b + 2.855e-4*t ) + 76.38e-12*t**3) * (1-por)/(1+por)/0.864
            return {'rho':rho, 'cp':cp, 'k':k}

        # na: liquid sodium
        elif inp['type'] == 'na':
            t = inp['t']
            # J.K. Fink and L. Leibowitz "Thermodynamic and Transport Properties of Sodium Liquid and Vapor", ANL/RE-95/2, 1995, https://www.ne.anl.gov/eda/ANL-RE-95-2.pdf
            rhol = 219.0 + 275.32*(1.0 - t/2503.7) + 511.58*(1.0 - t/2503.7)**0.5
            visl = math.exp(-6.4406 - 0.3958*math.log(t) + 556.835/t)/rhol
            kl = 124.67 - 0.11381*t + 5.5226e-5*t**2 - 1.1842e-8*t**3
            # Based on fit from J.K. Fink, et. al."Properties for Reactor Safety Analysis", ANL-CEN-RSD-82-2, May 1982.
            cpl = 1646.97 - 0.831587*t + 4.31182e-04*t**2
            return {'rhol':rhol, 'visl':visl, 'kl':kl, 'cpl':cpl}

        # lbe: liquid lead and bismuth (55%wt Bi, 45%wt Pb)
        elif inp['type'] == 'lbe':
            t = inp['t']
            # OECD, Nuclear Energy Agency, Handbook on Lead-bismuth Eutectic Alloy and Lead Properties, Materials Compatibility, Thermalhydraulics and Technologies, OECD, 2015. https://doi.org/10.1787/42dcd531-en.
            # density (kg/m3): @400K-1300K equation from "Handbook on Lead-bismuth Eutectic Alloy and Lead Properties", p.130, same as the following ones
            rhol = 11065-1.293*t
            # dynamic viscosity (Pa·s): @400K-1200K 
            visl = 4.94e-4*math.exp(754.1/t)
            # specific heat (J/kg-K): @400K-1100K 
            cpl = 164.8-3.94e-2*t+1.25e-5*t*t-4.56e5/t/t
            # thermal conductivity (W/m-K): @400K-1300K
            kl = 3.284 + 1.617e-2*t-2.305e-6*t*t
            return {'rhol':rhol, 'visl':visl, 'kl':kl, 'cpl':cpl}

        elif inp['type'] == 'h2o':
            t = inp['t']
            rhol = 864.70
            visl = 0.0001343
            cpl = 4493.74
            kl = 0.6634
            return {'rhol':rhol, 'visl':visl, 'kl':kl, 'cpl':cpl}

        # ss316: stainless steel type of 316
        elif inp['type'] == 'ss316':
            t = inp['t']
            # density (kg/m3): @300K equation from Leibowitz, et al, "Properties for LMFBR safety analysis", ANL-CEN-RSD-76-1 (1976), p.117
            rho = 7954.
            # specific heat (J/kg-K): Leibowitz, et al, "Properties for LMFBR safety analysis", ANL-CEN-RSD-76-1 (1976), p.100. Note that 1 mol of SS316 = 10.165 kg (https://www.webqc.org/molecular-weight-of-SS316.html) and 1 cal = 4.184 J
            cp = (6.181 + 1.788e-3*t)*10.165*4.184
            # thermal conductivity (W/m-K): Leibowitz, et al, "Properties for LMFBR safety analysis", ANL-CEN-RSD-76-1 (1976), p.100.
            k = 9.248 + 1.571e-2*t
            return {'rho':rho, 'cp':cp, 'k':k}

        # bn: boron nitide
        elif inp['type'] == 'bn':
            t = inp['t']
            tc = t -273.15
            # density (kg/m3): I.Di Piazza, et al., Benchmark specifications for NACIE-UP facility: non-uniform power distribution tests, ENEA Report, NA-I-R-542, Feb. 2023
            rho = 2000.
            # specific heat (J/kg-K): I.Di Piazza, et al., Benchmark specifications for NACIE-UP facility: non-uniform power distribution tests, ENEA Report, NA-I-R-542, Feb. 2023
            cp = 800.
            # thermal conductivity (W/m-K): I.Di Piazza, et al., Benchmark specifications for NACIE-UP facility: non-uniform power distribution tests, ENEA Report, NA-I-R-542, Feb. 2023
            k = 25.578 - 2.416*math.log(tc)
            return {'rho':rho, 'cp':cp, 'k':k}

        # cu: copper
        elif inp['type'] == 'cu':
            t = inp['t']
            # density (kg/m3): I.Di Piazza, et al., Benchmark specifications for NACIE-UP facility: non-uniform power distribution tests, ENEA Report, NA-I-R-542, Feb. 2023
            rho = 8933.
            # specific heat (J/kg-K): I.Di Piazza, et al., Benchmark specifications for NACIE-UP facility: non-uniform power distribution tests, ENEA Report, NA-I-R-542, Feb. 2023
            cp = 385.
            # thermal conductivity (W/m-K): I.Di Piazza, et al., Benchmark specifications for NACIE-UP facility: non-uniform power distribution tests, ENEA Report, NA-I-R-542, Feb. 2023
            k = 401
            return {'rho':rho, 'cp':cp, 'k':k}

    #----------------------------------------------------------------------------------------------
    # Nusselt number: self is a 'data' object created in B, inp is a dictionary of input data dependent on the case
    def nu(self, inp):

        pe = inp['pe']
        if 'p2d' in inp:
            # pin bundle
            p2d = inp['p2d']
            # forced convection in a pin bundle (Mikityuk, NED 2008)
            return 0.047*(1.0-math.exp(-3.8*(p2d-1.0))) * ((pe)**0.77 + 250.0)
            
        else:
            # round tube
            return 4.8 + 0.025 * (pe)**0.8

    #----------------------------------------------------------------------------------------------
    # Friction factor: self is a 'data' object created in B, inp is a dictionary of input data dependent on the case
    def fricfac(self, re):

        if re == 0:
            return 1e30
        elif re <= 2000:
            # laminar friction factor
            return 64/re
        elif re > 4000:
            # turbulent friction factor
            return 0.316/re**0.25
        else:
            # transition friction factor
            return 0.032 + 0.0077*(re/2000 - 1)
