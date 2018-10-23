from metspy.dispatcher import Dispatcher

def main():
	disp = Dispatcher(start_hour = "13")
	disp.cust_run("./static/urls1.pkl")
	disp.deft_run(country_name = "Argentina")

if __name__ == '__main__':
	main()
