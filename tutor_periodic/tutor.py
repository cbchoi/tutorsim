import contexts

from tutorsim.system_simulator import SystemSimulator
from tutorsim.behavior_model_executor import BehaviorModelExecutor
from tutorsim.system_message import SysMessage
from tutorsim.definition import *

from my_generator import Generator
from my_processor import Processor
from my_assessor import Assessor

from config import *
from instance.config import *

se = SystemSimulator()

SystemSimulator().register_engine("sname", SIMULATION_MODE)

g = Generator(0, Infinite, "Peter", "sname")
p = Processor(0, Infinite, "Mat", "sname")
a = Assessor(0, Infinite, "Simon", "sname")

SystemSimulator().get_engine("sname").insert_input_port("start")
SystemSimulator().get_engine("sname").insert_input_port("report")
SystemSimulator().get_engine("sname").register_entity(g)
SystemSimulator().get_engine("sname").register_entity(p)
SystemSimulator().get_engine("sname").register_entity(a)

SystemSimulator().get_engine("sname").coupling_relation(None, "start", g, "start")
SystemSimulator().get_engine("sname").coupling_relation(None, "report", a, "report")

SystemSimulator().get_engine("sname").coupling_relation(g, "process", p, "process")
SystemSimulator().get_engine("sname").coupling_relation(p, "assess", a, "assess")
SystemSimulator().get_engine("sname").insert_external_event("start", STUDENT_LIST_SOURCE)
SystemSimulator().get_engine("sname").simulate()
print("!")
SystemSimulator().get_engine("sname").insert_external_event("report", ASSESSMNET_DESTINATION)
SystemSimulator().get_engine("sname").simulate()
