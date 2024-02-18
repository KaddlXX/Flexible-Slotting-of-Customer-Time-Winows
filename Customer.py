class Customer:
    def __init__(self, id, xCoord, yCoord, custType, date, time, willingToWait, deliveryWindows, priceSens, satisfaction= "Very Satisfied", sReason="", orderPrice="none"):
        self.id = id
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.custType = custType
        self.date = date
        self.time = time
        self.willingToWait = willingToWait #boolean
        self.deliveryWindows = deliveryWindows #list
        self.priceSens = priceSens          #boolean
        self.satisfaction = satisfaction
        self.sReason = sReason
        self.orderPrice = orderPrice


    def __str__(self):
        string = (
            f"id:{type(self.id)} {self.id}\n"
            f"xCoord:{type(self.xCoord)} {self.xCoord}\n"
            f"yCoord:{type(self.yCoord)} {self.yCoord}\n"
            f"custType:{type(self.custType)} {self.custType}\n"
            f"date:{type(self.date)} {self.date}\n"
            f"time:{type(self.time)} {self.time}\n"
            f"willingToWait:{type(self.willingToWait)} {self.willingToWait}\n"
            f"deliveryWindows:{type(self.deliveryWindows)} {self.deliveryWindows}\n"
            f"priceSens:{type(self.priceSens)} {self.priceSens}\n"
            f"satisfaction:{type(self.satisfaction)} {self.satisfaction}\n"
            f"sReason:{type(self.sReason)} {self.sReason}\n"
            f"orderPrice:{type(self.orderPrice)} {self.orderPrice}\n"

        )
        return string
