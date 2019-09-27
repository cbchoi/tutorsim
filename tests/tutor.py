import contexts

from tutorsim.system_simulator import SystemSimulator
from tutorsim.behavior_model_executor import BehaviorModelExecutor
from tutorsim.system_message import SysMessage
from tutorsim.definition import *

from tutorsim.generator import Generator
from tutorsim.processor import Processor
from tutorsim.assessor import Assessor


se = SystemSimulator()

SystemSimulator().register_engine("sname")

g = Generator(0, 100, "Peter", "sname")
p = Processor(0, Infinite, "Mat", "sname")
a = Assessor(0, Infinite, "Simon", "sname")

SystemSimulator().get_engine("sname").insert_input_port("start")
SystemSimulator().get_engine("sname").register_entity(g)
SystemSimulator().get_engine("sname").register_entity(p)
SystemSimulator().get_engine("sname").register_entity(a)

SystemSimulator().get_engine("sname").coupling_relation(None, "start", g, "start")
SystemSimulator().get_engine("sname").coupling_relation(g, "process", p, "process")
SystemSimulator().get_engine("sname").coupling_relation(p, "assess", a, "assess")
SystemSimulator().get_engine("sname").insert_external_event("start", "student_list.csv")
SystemSimulator().get_engine("sname").simulate()