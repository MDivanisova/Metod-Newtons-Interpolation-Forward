import math

# C:\Users\mynig\Desktop\macka_vp\Num metod\important.txt


def get_data_from_user():  #citanje od tastatura
    n = int(input("Внеси број на податоци: "))
    x, y = [], []

    print("Внеси ги податоците :")
    for i in range(n):
        xi = float(input(f"x[{i}] = "))
        yi = float(input(f"y[{i}] = "))
        x.append(xi)
        y.append(yi)
    return x, y


def get_data_from_file(file_path):
    # citanje od txt dokument
    x, y = [], []
    try:
        with open(file_path, 'r') as file: #otvaranje na txt dokument za da go citame
            for line in file:
                xi, yi = map(float, line.split()) #deleme ja linijata na dve vrednosti i toa go konvertirame vo float
                x.append(xi)
                y.append(yi)
    except FileNotFoundError: #obrabotka na greskata ako dokumento ne postoe
        print(f"Грешка: Не постои документот {file_path}.") #izvestuvanje za greskata
        return None, None
    return x, y


def create_delta_y(arr_y): #funkcija za kreiranje na niza od deltta y
    delta_y = [arr_y[0]] #inicijalizacija na niza delta y so prvata vrednost od arry_y
    temp_y = []
    while len(temp_y) != 1: #ja izminuvame privremenata niza se dodeka ne dojdeme do 1 element
        temp_y = []
        for i in range(len(arr_y) - 1): #for ciklus koj odi se do pretposlednio element na glavnata niza
            temp_y.append(arr_y[i + 1] - arr_y[i])
        delta_y.append(temp_y[0]) #dodavanje na prvata razlika sto sme ja dobile vo temp_y vo delta_y
        arr_y = temp_y #sega glavnata niza ni gi sodrzi elementite od privremenata niza
    return delta_y


def calculate_result(delta_y, alpha): #funkcija za presmetuvanje na rezultatot so elementite of delta_y i alfa
    result = 0
    for i in range(len(delta_y)): #izminuvanje na site elementi od nizata delt_y
        alpha_final = 1
        for j in range(i):
            alpha_final = alpha_final * (alpha - j) #go sozdavame alpha
        result = result + 1 / math.factorial(i) * delta_y[i] * alpha_final #del od finalnio rezlutat
    return result


def is_h_same(x):  #funkcija za proverka dali razlikata megju elementite od nizata
    temp_h = x[1] - x[0]
    for i in range(len(x) - 1):  #ja izminuvame nizata odekji do pretposlednio element
        if x[i + 1] - x[i] != temp_h:  #proveruvame na sekoj sleden par dali rastojanieto e razlicno
            return False, None
    return True, temp_h


def is_in_first_half(x, find_x):  #funkcija koja proveruva dali baranio podatok se naogja u prvata polovina
    for i in range(int(len(x)/2) + 1):
        if x[i] < find_x < x[i + 1]:
            return True
    return False


def error_estimation(delta_y_len, delta_y_n, alpha):  #funkija za presmetuvanje na greskata
    alpha_final = 1
    for j in range(delta_y_len):
        alpha_final = alpha_final * (alpha - j)
    result = (abs(delta_y_n) / math.factorial(delta_y_len)) * abs(alpha_final)
    return result


if __name__ == "__main__":

    print("Избери како сакаш да ги внесеш податоците:")
    print("1. Рачно внесување")
    print("2. Читање од .txt документ")

    choice = input("Твој избор е: ")
    x, y, find_x = [], [], 0
    if choice == '1':  #dobivanje na nizite so racno vnesuvanje
        x, y = get_data_from_user()

    elif choice == '2':  #dobivanje na nizite od txt dokument
        file_path = input("Внеси го патот до .txt документот: ")
        x, y = get_data_from_file(file_path)
        if x is None or y is None:
            print("Нема податоци во документот.")

    else:
        print("Невалиден избор!")

    find_x = float(input("Внеси податок за кој да се пронајде неговата вредност: "))
    print("Избери дали сакате пресметката да биде со целото множество:")
    print("1. Да")
    print("2. Не")
    choice = input("Твој избор е: ")

    is_h_same, h = is_h_same(x)

    if is_h_same:  #dokolku rastojanieto ni e isto prodolzuvame so narednite ispituvanja
        if is_in_first_half(x, find_x) is False:  #malo predupreduvanje
            print("Внимание податокот се наогја во втората половина на низата од податоци препорака е да се користи "
                  "Нјутнова интерполација назад.")
        created_delta_y_full = create_delta_y(y)  #dobivanje na delta y nizata
        alpha = (find_x - x[0]) / h  #dobivanje na alpha
        if choice == '1':
            print(f"Резултатот е следниот: {calculate_result(created_delta_y_full, alpha)}")
        if choice == '2':
            if len(x) % 2 == 0:  #dobivanje na x i y vo zavisnost od toa dali nizata e parna ili neparna
                halfed_x = x[0:int(len(x) / 2)]
                halfed_y = y[0:int(len(y) / 2)]
            else:
                halfed_x = x[0:(int(len(x) / 2) + 1)]
                halfed_y = y[0:(int(len(y) / 2) + 1)]

            created_delta_y = create_delta_y(halfed_y)  #dobivanje na delta y od pola niza
            print(f"Резултатот е следниот: {calculate_result(created_delta_y, alpha)}")
            element_index = len(created_delta_y)  #dobivanje na indexot sto ni treba pri presmetuvanje na greskata
            print(f"Проценката на грешката е: {error_estimation(element_index, created_delta_y_full[element_index], alpha)}")
    else:
        print("Податоците немаат исто растојание, употребете ја лангранжовата интерполација.")
