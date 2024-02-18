class Timeslot:
    def __init__(self, id, start, end, price):
        self.id = id
        self.start = start
        self.end = end
        self.price = price
        self.customerList = []
        self.isFree = True

    #def __str__(self):
    #    return f"{self.id} - {self.start} - {self.end} - {self.price} - {self.customerList} - {self.isFree}"

    def __str__(self):
        string = (
            f"id:           {self.id}\n"
            f"start:        {self.start}\n"
            f"end:          {self.end}\n"
            f"price:        {self.price}\n"
            f"customerList: {self.customerList}\n"
            f"isFree:       {self.isFree}\n\n"
        )
        return string

    def appendToCustomerList(self, appendix):
        setattr(self, "customerList", appendix)
