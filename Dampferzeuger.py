from tespy.networks import Network
from tespy.components import (Source, Sink, DiabaticCombustionChamber, Turbine, Compressor)
from tespy.connections import Connection, Bus, Ref
from CoolProp.CoolProp import PropsSI as CPSI
from tespy.tools import ExergyAnalysis

# fluids
H20 = 'water'
fld_H20 = {H20: 1}

oxygen = 'O2'
nitrogen = 'N2'
air = 'air'
fld_air = {oxygen: 0.21, nitrogen: 0.79}

gas = 'CH4'
fld_gas = {gas: 1}

# network Brennkammer mit Turbine
combastion = Network(T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s')

# components of system
cmp_cp = Compressor('Compressor')
cmp_cc = DiabaticCombustionChamber('combustion chamber')
cmp_tb = Turbine('Turbine')
src_air = Source('air source')
src_gas = Source('fuel source')
snk_fg = Sink('flue gas sink')

# components Data
cmp_cp.set_attr(eta_s=0.8, pr=1)
cmp_tb.set_attr(eta_s=0.9)
cmp_cc.set_attr(pr=1, eta=1, lamb=1.05)

# connection 1
c01 = Connection(src_air, 'out1', cmp_cp, 'in1', label='01')
c01.set_attr(p=1, T=15, fluid=fld_air)

# connection 2
c02 = Connection(cmp_cp, 'out1', cmp_cc, 'in1', label='02')
c02.set_attr(p=30)

# connection 3
c03 = Connection(src_gas, 'out1', cmp_cc, 'in2', label='03')
c03.set_attr(T=15, fluid=fld_gas, m=1)  # Setzen eines kleinen Massenstroms als Startwert

# connection 4
c04 = Connection(cmp_cc, 'out1', cmp_tb, 'in1', label='04')
#c04.set_attr(T=1600)

# connection 5
c05 = Connection(cmp_tb, 'out1', snk_fg, 'in1', label='05')
c05.set_attr(p=1)

combastion.add_conns(c01, c02, c03, c04, c05)

# results
combastion.solve(mode='design')
combastion.print_results()
