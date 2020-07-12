# names
# subtotal (before taxes * tip)
# total
# did x have any item to themselves?
# did x skip out on any item?
from collections import OrderedDict
from decimal import Decimal


def get_names():
	return raw_input("Enter names separated by comma: ").split(',')


def get_subtotal():
	subtotal = raw_input("Enter subtotal (amount before taxes and tip): ")
	return float(subtotal.strip('$'))


def get_total():
	total = raw_input("Enter order total: ")
	return float(total.strip('$'))


def format_list(listy):
	if len(listy) == 1:
		return listy[0]
	if len(listy) == 2:
		return "{} and {}".format(", ".join(listy[:-1]),  listy[-1])
	if len(listy) > 2:
		return "{}, and {}".format(", ".join(listy[:-1]),  listy[-1])


def determine_sharing(names):
	# GATHER WHO HAD WHAT
	unequally_shared_items = raw_input("List the names of all items (separated by comma) that weren't shared by everyone: ").split(',')
	unequally_shared_items = dict.fromkeys(unequally_shared_items, {})
	custom_split = OrderedDict()
	for item in unequally_shared_items:
		consumers = []
		print "\n"
		for person in names:
			had_some = raw_input("Did " + person + " have " + item + "? (y/n): ")
			if had_some == 'y':
				consumers.append(person)
		price = raw_input("How much was the " + item + "?: ").strip('$')
		custom_split[item] = {"consumers": consumers, "price": price}

	# SUMMARY OF SPLIT
	print "\n########################################################"
	print("Here's who had what: \n")
	for item,details in custom_split.iteritems():
		print(item.capitalize() + " was shared by " + format_list(details.get("consumers")))
		print "Price: $" + details.get("price") + "\n"

	print "The remaining items were shared by everyone."
	print "########################################################"

	verify = raw_input("\nIs this correct? (y/n): ")
	if verify == 'n':
		determine_sharing(names)

	return custom_split


def calculate_bill(names, custom_split):
	subtotal = get_subtotal()
	total = get_total()
	balance = dict.fromkeys(names, 0)
	cost_shared_by_all = subtotal
	tax_tip = total-subtotal
	for item,details in custom_split.iteritems():
		number_of_sharers = len(details.get("consumers"))
		price = float(details.get("price"))
		split_amount = price/number_of_sharers
		cost_shared_by_all -= price

		for person in details.get("consumers"):
			balance[person] += split_amount

	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print "Here's the final bill split:\n"

	for name,amount in balance.iteritems():
		balance[name] += cost_shared_by_all/len(balance)
		balance[name] += tax_tip*(balance[name]/subtotal)
		print name + " owes $" + "{:.2f}".format((balance[name]))
	print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"


def main():
	names = get_names()
	custom_split = determine_sharing(names)
	calculate_bill(names, custom_split)


if __name__ == "__main__":
	main()


