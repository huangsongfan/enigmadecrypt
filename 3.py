# class definition
class rotor:
    # properties
    input_order = list()
    output_order = list()

    # constructor of rotor class
    def __init__(self):
        im_an_inverter = False;
        modulus = -1

    # destructor of rotor class
    def __del__(self):
        if self.modulus < 0:
            return
        del self.input_order
        del self.output_order

    # turnover function
    def turnover(self, i):
        i += 1
        # perform i mod modulus operation if i > modulus
        if i >= self.modulus:
            i %= self.modulus
            return True
        return False

    # symbol_from_index function
    def symbol_from_index(self, i):
        return self.input_order[i]

    # inverting function
    # returns im_an_inverter
    def inverting(self):
        return self.im_an_inverter

    # load function, load values to rotor class
    def load(self, input, output, inv):
        self.im_an_inverter = inv

        # put length of input to modulus
        self.modulus = len(input)

        # iterate through modulus
        for i in range(0,self.modulus):
            if(output[i]) == None:
                self.modulus = -1
                return False

        count = 0
        #  count the number where output and input are the same
        for i in range(0, self.modulus):
            for j in range(0,self.modulus):
                if output[j] == input[i]:
                    count += 1

            if self.im_an_inverter and output[i] == input[i]:
                self.modulus = -1
                return False

        if count != self.modulus:
            return False

        self.input_order = [None] * self.modulus
        self.output_order = [None] * self.modulus

        if not self.im_an_inverter:
            for i in range(0, self.modulus):
                self.input_order[i] = input[i]
                self.output_order[i] = output[i]

            return True
        # put input into input_order
        for i in range(0,self.modulus):
            self.input_order[i] = input[i]
        # put output into output_order
        for i in range(0,self.modulus):
            self.output_order[i] = None

        for i in range(0,self.modulus):
            if self.output_order[i] != None:
                continue

            if self.output_order[self.index_from_symbol(output[i])] != None:
                continue

            self.output_order[i] = output[i]

            for j in range(0, self.modulus):
                if self.input_order[j] == self.output_order[i]:
                    if self.output_order[j] != None:
                        continue
                    self.output_order[j] = self.input_order[i];

                    break;

        for i in range(0,self.modulus):
            if self.output_order[i] == None:
                self.output_order[i] = self.input_order[i]


        return True


    # forward function
    def forward(self,a, offset):

        if (self.im_an_inverter):
            offset = 0

        who = 0
        for who in range(0,self.modulus):
            if self.input_order[who] == a:
                break

        who += offset
        who = who % self.modulus
        return self.output_order[who]

    # reverse function
    def reverse(self, a, offset):
        if self.im_an_inverter:
            offset = 0
        who = 0

        for who in range(0,self.modulus):
            if self.output_order[who] == a:
                break

        who -= offset

        if who < 0:
            who += self.modulus

        who = who % self.modulus

        return self.input_order[who]

    # index_from_symbol function
    def index_from_symbol(self, a):
        for i in range(0, self.modulus):
            if self.input_order[i] == a:
                return i

        return -1

# calculator_Phi function
def Calculator_Phi(infile, total):
    # initialize variables
    Frequency_Count = [0] * 30
    count_Array = [0] * 30
    Frequency_Count_Char = [None] * 30
    size = 0
    totalChars = 0
    flag = 0
    pos = 0
    i = 0
    j = 0
    Frequency_Count[0] = 1
    Frequency_Count_Char[0] = infile[0]

    i += 1

    # initialize Value_Phi
    Value_Phi = 0.0

    # calculate the frequency of characters
    for k in range(1, total):
        Char_Input = infile[k]
        if Char_Input.isalpha():
            for j in range(0, i):
                if Char_Input == Frequency_Count_Char[j]:
                    flag = 1
                    pos = j
                    break

            if flag == 1:
                Frequency_Count[pos] = Frequency_Count[pos] + 1
                flag = 0
            else:
                Frequency_Count[i] = 1
                Frequency_Count_Char[i] = Char_Input
                i += 1

    for j in range(0,i):
        count_Array[j] = float(Frequency_Count[j])/float(total)

    for j in range(0,i):
        Value_Phi += float(count_Array[j]) * (float(count_Array[j]) - (1.0/float(total)))

    return Value_Phi


# main function
if __name__ == '__main__':
    # initialize variables
    Rotor_Max = 10
    output = [''] * 600
    Input_Cipher = [None] * 600
    # bank = [rotor()] * 10
    bank_0 = rotor()
    bank_1 = rotor()
    bank_2 = rotor()
    bank_9 = rotor()
    highest_Phi = 0.0
    rotor1_key = 0
    rotor2_key = 0
    rotor3_key = 0
    # load data to rotor instances
    bank_0.load("abcdefghijklmnopqrstuvwxyz", "abcghidefjklpqrmnostxyzuvw", False)
    bank_1.load("abcdefghijklmnopqrstuvwxyz", "defghijklmnopqrstuvwxyzabc", False)
    bank_2.load("abcdefghijklmnopqrstuvwxyz", "zxbcdefghijklnmpqosrtuvway", False)
    bank_9.load("abcdefghijklmnopqrstuvwxyz", "zyabcdefghijklmnopqrstxwuv", True)

    # read the encrypted message from the file
    input_File = open("cipher.txt")

    ins = 0

    Input_Cipher = input_File.read()

    ins = len(Input_Cipher)
    Value_Phi = 0.0

    position_0 = 0
    position_1 = 0
    position_2 = 0
    position_3 = 0

    # iterate through the rotors
    for i in range(0, 26):
        for j in range(0, 26):
            for k in range(0, 26):
                for l in range(0, ins):
                    Rotor_Char_Return_Value = bank_0.forward(Input_Cipher[l], position_0)
                    Rotor_Char_Return_Value = bank_1.forward(Rotor_Char_Return_Value, position_1)
                    Rotor_Char_Return_Value = bank_2.forward(Rotor_Char_Return_Value,position_2)
                    Rotor_Char_Return_Value = bank_9.forward(Rotor_Char_Return_Value, 0)
                    Rotor_Char_Return_Value = bank_2.reverse(Rotor_Char_Return_Value, position_2)
                    Rotor_Char_Return_Value = bank_1.reverse(Rotor_Char_Return_Value, position_1)
                    Rotor_Char_Return_Value = bank_0.reverse(Rotor_Char_Return_Value, position_0)

                    position_2 += 1
                    if position_2 == 26:
                        position_2 = 0
                        position_1 += 1

                        if position_1 == 26:
                            position_1 = 0
                            position_0 += 1

                            if position_0 == 26:
                                position_0 = 0

                    output[l] = Rotor_Char_Return_Value

                Value_Phi = Calculator_Phi(output, ins)

                if Value_Phi > 0.06:
                    print("Value Of Phi: " + str(Value_Phi) + "\n")
                    print("Rotor 1:" + str(position_0) + ", Rotor 2:" + str(position_1) + "Rotor 3:" + str(position_2) + "\n")

                    if highest_Phi < Value_Phi:
                        highest_Phi = Value_Phi
                        rotor1_key = position_0
                        rotor2_key = position_1
                        rotor3_key = position_2

                position_2 = k

            position_1 = j

        position_0 = i

    # print out the key and decrypted message
    print("Largest Phi Value is " + str(highest_Phi) + "\n")
    print("Rotor 1:" + str(rotor1_key) + "Rotor 2:" + str(rotor2_key) + "Rotor 3:" + str(rotor3_key))
    print(
        "\n-------------------------------------------------------------------------------------------------------\n");
    print("Decrypted Text is:\n");

    print(''.join(output))












