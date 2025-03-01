import simpy
import random

class PrintingFarm:
    def __init__(self, env, num_printers):
        self.env = env
        self.printer = simpy.Resource(env, num_printers) 
        self.post_process = simpy.Resource(env, 5)  # 후공정 장비 5대
        self.inspection = simpy.Resource(env, 3)  # 검사 장비 3대

    def print_part(self, order_id):
        with self.printer.request() as req:
            yield req
            print(f"[{self.env.now}] 주문 {order_id}: 프린팅 시작")
            yield self.env.timeout(random.randint(30, 60))
            print(f"[{self.env.now}] 주문 {order_id}: 프린팅 완료")

    def post_process_part(self, order_id):
        with self.post_process.request() as req:
            yield req
            print(f"[{self.env.now}] 주문 {order_id}: 후공정 시작")
            yield self.env.timeout(random.randint(10, 20))
            print(f"[{self.env.now}] 주문 {order_id}: 후공정 완료")

    def inspect_part(self, order_id):
        with self.inspection.request() as req:
            yield req
            print(f"[{self.env.now}] 주문 {order_id}: 검사 시작")
            yield self.env.timeout(random.randint(5, 15))
            print(f"[{self.env.now}] 주문 {order_id}: 검사 완료")

    def process_order(self, order_id):
        yield self.env.process(self.print_part(order_id))
        yield self.env.process(self.post_process_part(order_id))
        yield self.env.process(self.inspect_part(order_id))
        print(f"[{self.env.now}] 주문 {order_id}: 납품 완료")

def order_generator(env, factory):
    order_id = 1
    while True:
        yield env.timeout(random.randint(10, 30))
        env.process(factory.process_order(order_id))
        order_id += 1

env = simpy.Environment()
factory = PrintingFarm(env, num_printers=5)
env.process(order_generator(env, factory))
env.run(until=200)
