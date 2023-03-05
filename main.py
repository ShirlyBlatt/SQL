from persistence import *
import sys
import atexit


def config(file_path, repo):
    with open(file_path) as config_file:
        first_line = config_file.readline()
        hats_num = int(first_line[0:first_line.find(',')])
        suppliers_num = int(first_line[first_line.find(',') + 1:])
        for line in config_file.readlines():
            if hats_num > 0:
                hat_info = line.split(',')
                hat = Hat(*hat_info)
                repo.hats.insert(hat)
                hats_num -= 1
            elif suppliers_num > 0:
                supplier_info = line.split(',')
                supplier = Supplier(*supplier_info)
                repo.suppliers.insert(supplier)
                suppliers_num -= 1


def order(file_path, repo, summary_file_location):
    with open(file_path) as order_file:
        order_id = 1
        for line in order_file.readlines():
            order_info = line.split(',')
            order_location = order_info[0]
            order_topping = order_info[1].rstrip("\n")
            hat = repo.hats.select_hat(order_topping)
            if hat:
                # insert to orders table
                order_obj = Order(order_id, order_location, hat.hat_id)
                repo.orders.insert(order_obj)
                repo.hats.update_quantity(hat.hat_id)
                order_id += 1
                supplier = repo.suppliers.find(hat.supplier)
                # write to summary file
                summary(summary_file_location, order_topping + ',' + supplier.supplier_name + ',' + order_location)


def summary(file_path, line):
    with open(file_path, 'a') as summary_file:
        summary_file.write(line + "\n")


def main():
    repo = Repository(sys.argv[4])
    repo.crate_tables()
    config(sys.argv[1], repo)
    order(sys.argv[2], repo, sys.argv[3])
    atexit.register(repo.close)


if __name__ == '__main__':
    main()
