import machine


class accel():
    def __init__(self, i2c, addr=0x68):
        self.iic = i2c
        self.addr = addr
        self.iic.start()
        self.iic.writeto(self.addr, bytearray([107, 0])) 
        self.iic.writeto_mem(self.addr, 0x1C, bytearray([255]))
        print(self.iic.readfrom_mem(self.addr, 0x1C, 1))
        self.iic.stop()

    def get_raw_values(self):
        self.iic.start()
        a = self.iic.readfrom_mem(self.addr, 0x3B, 14)
        self.iic.stop()
        return a

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values(self):
        raw_ints = self.get_raw_values()
        vals = {}
        vals["AcX"] = self.bytes_toint(raw_ints[0], raw_ints[1])
        vals["AcY"] = self.bytes_toint(raw_ints[2], raw_ints[3])
        vals["AcZ"] = self.bytes_toint(raw_ints[4], raw_ints[5])
        #vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9])
        vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11])
        vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
        return vals  # returned in range of Int16
        # -32768 to 32767

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        while 1:
            print(self.get_values())
            sleep(0.05)
            
    def calibrate(threshold=50, n_samples=100):
        '''
        Get calibration date for the sensor, by repeatedly measuring
        while the sensor is stable. The resulting calibration
        dictionary contains offsets for this sensor in its
        current position.
        '''
        while True:
            v1 = accel.get_values()
            v2 = accel.get_values()
            # Check all consecutive measurements are within
            # the threshold. We use abs() so all calculated
            # differences are positive.
            if all(abs(v1[k] - v2[k]) < threshold for k in v1.keys()):
                return v1  # Calibrated.

    
    
    def get_smoothed_values(n_samples=10):

        for _ in range(samples):
           data = accel.get_values()

           for key in data.keys():
            # Add on value / samples (to generate an average)
            # with default of 0 for first loop.
               result[m] = result.get(m, 0) + (data[m] / samples)
               return result
