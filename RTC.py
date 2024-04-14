# Component Datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/ds1307.pdf
# I2C API documentation: https://docs.micropython.org/en/latest/library/machine.I2C.html

class RTC(object):
    def __init__(self, i2c: I2C, address: Optional[int] = None, initial_date: Optional[string] = None, initial_time: Optional[string] = None) -> None:
        """
        Constructs a new instance and configures the RTC to start counting from 01/01/2000 00:00:00

        :param      i2c:        I2C object for the bus the RTC is attached to
        :type       i2c:        I2C
        :param      address:    The I2C bus address of the RTC
        :type       address:    Optional int
        """
        self.i2c = i2c
        self.address = address if address else 0x68
        self.memory_buffer = bytearray(7)

        # Address of the timekeeping register
        self.timekeeping_register = 0x00

        # Initialize the initiale date and time
        self.initial_date = initial_date if initial_date else '01/01/2000'
        self.initial_time = initial_time if initial_time else '00:00:00'

        self.initialize_datetime(self.initial_date, self.initial_time)


    def tokenize_datetime(self, date_string, time_string):
        """
        Tokenize the the date and time strings to obtain the integer values

        :param      initial_date:   The desired date_string to be tokenized, in the structure DD/MM/YYYY
        :type       string:         string
        :param      initial_time:   The desired time_string to be tokenized, in the structure HH:MM:SS
        :type       datetime:       string

        :returns:   (HH, MM, SS, DD, MM, YYYY)
        :rtype:     Tuple[int, int, int, int, int, int]
        """

        # Tokenize the date_string and convert to integers
        day, month, year = map(int, date_string.split('/'))

        # Tokenize the time_string and convert to integers
        hours, minutes, seconds = map(int, time_string.split(':'))

        # Return the tuple of values
        return(hours, minutes, seconds, day, month, year) 

    def initialize_datetime(self, initial_date, initial_time) -> None:
        """
        Sets the current datetime in the RTC. The structure of the Tuple is as follows:
        (HH, MM, SS, DD, MM, YYYY)

        :param      initial_date:   The desired initial_date to be set, in the structure DD/MM/YYYY
        :type       string:         string
        :param      initial_time:   The desired initial_date to be set, in the structure HH:MM:SS
        :type       datetime:       string
        """
        # Extract token from the date and time strings, make it a tuple
        self.initial_datetime = self.tokenize_datetime(initial_date, initial_time)

        #  Set the time to the initial values, return true or false
        time_set = self.set_datetime(self.initial_datetime)

        if time_set:
            print("Time successfully initialized to {} {}".format(initial_date, initial_time))

        else:
            print("Time initialization unsuccessful")


    
    def set_datetime(self, datetime: Tuple[int, int, int, int, int, int]) -> bool:
        """
        Sets the current datetime in the RTC. The structure of the Tuple is as follows:
        (HH, MM, SS, DD, MM, YYYY)

        :param      datetime:   The desired datetime to be set, in the structure (HH, MM, SS, DD, MM, YYYY)
        :type       datetime:   Tuple[int, int, int, int, int, int]

        :returns:   True if datetime was successfully set, False otherwise
        :rtype:     bool
        """
        # Convert the input datetime into BCD and save in memory buffer
        self.memory_buffer[0] = self.int_to_bcd(datetime[2] ) # seconds
        self.memory_buffer[1] = self.int_to_bcd(datetime[1] ) # minutes
        self.memory_buffer[2] = self.int_to_bcd(datetime[0] ) # hours
        self.memory_buffer[4] = self.int_to_bcd(datetime[3] ) # days
        self.memory_buffer[5] = self.int_to_bcd(datetime[4] ) # months
        self.memory_buffer[6] = self.int_to_bcd(datetime[5] % 100) # years
        
        # Write from memory buffer to the RTC Timekeeping register
        self.i2c.writeto_mem(self.address, self.timekeeping_register, self.memory_buffer)
        
        # Get the time from the RTC
        set_time = self.get_datetime()

        # If the set time equals the obtined time, return true
        if (set_time[0] == datetime[0] and set_time[1] == datetime[1] and 
            set_time[2] == datetime[2] and set_time[3] == datetime[3] and 
            set_time[4] == datetime[4] and set_time[5] == datetime[5]):
            return True
        # Else return flae
        return False

    def get_datetime(self) -> Tuple[int, int, int, int, int, int]:
        """
        Fetch the current datetime stored in the RTC
        
        :returns:   (HH, MM, SS, DD, MM, YYYY)
        :rtype:     Tuple[int, int, int, int, int, int]
        """

        # Read from the RTC Timekeeping register into the Memory Buffer
        self.i2c.readfrom_mem_into(self.address, self.timekeeping_register, self.memory_buffer)

        # Check the time format, if it is 24 hour and if it is AM/PM
        format_24_hr = False if (self.memory_buffer[2] & 0x40) else True
        PM_time     = True if (self.memory_buffer[2] & 0x20) else False
    	
        # Extract the values from the memory buffer and convert from BCD into integers
        seconds = self.bcd_to_int(self.memory_buffer[0] & 0x7F)  # seconds
        minutes = self.bcd_to_int(self.memory_buffer[1]) # minutes
        hours   = 0 # hours
        if format_24_hr:
            hours = self.bcd_to_int(self.memory_buffer[2]) # if it is 24 hour format, return the value
        else:
            hours = self.bcd_to_int((self.memory_buffer[2] & 0x1F))
            if PM_time:
                hours = hours + 12
        
        day     = self.bcd_to_int(self.memory_buffer[4]) # day
        month   = self.bcd_to_int(self.memory_buffer[5]) # month
        year    = self.bcd_to_int(self.memory_buffer[6]) + 2000 # year

        return (hours, minutes, seconds, day, month, year)

    def bcd_to_int(self, bcd):
        """
        Convert binary-coded decimal to integer.

        :returns:   integer_value
        :rtype:     int
        """
        integer_value = (bcd >> 4) * 10 + (bcd & 0x0F)
        return integer_value
    
    def int_to_bcd(self, decimal):
        """Convert decimal to binary-coded decimal.
        
        :returns:   bcd_value
        :rtype:     BCD
        """
        bcd_value =  ((decimal // 10) << 4) + (decimal % 10)
        return bcd_value
