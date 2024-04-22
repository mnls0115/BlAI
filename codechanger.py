def prepare_code_for_json(input_path, output_path):
    try:
        # 파일을 읽기 모드로 열기
        with open(input_path, 'r') as file:
            # 모든 줄을 읽고, 개행 문자를 \n으로 치환
            lines = file.readlines()
            single_line = '\\n'.join(line.strip() for line in lines)

        # 큰따옴표를 이스케이프 처리
        escaped_line = single_line.replace('"', '\\"')

        # 결과를 새 파일에 저장
        with open(output_path, 'w') as file:
            file.write(escaped_line)
        print("Conversion and escaping successful. Data written to", output_path)
    except Exception as e:
        print("An error occurred:", e)

# 예제 사용법
input_path = 'codechange.py'  # 원본 코드 파일
output_path = 'code_single.txt'  # JSON에 저장할 준비가 된 파일

# 함수 호출
prepare_code_for_json(input_path, output_path)

"""
아래는 load 하는 함수
import json

def load_and_execute_code_from_json(json_path, key):
    try:
        # JSON 파일 열기
        with open(json_path, 'r') as file:
            code_data = json.load(file)
        
        # 지정된 키에 해당하는 코드 가져오기
        code_to_execute = code_data.get(key)
        if code_to_execute:
            # 코드 실행
            exec(code_to_execute)
            print("Code execution successful.")
        else:
            print(f"No code found for key: {key}")
    except Exception as e:
        print("An error occurred while executing the code:", e)

# 예제 사용법
json_path = 'main_for_json.txt'  # JSON 파일 경로
key = 'main.py'  # JSON 파일 내에서 실행하고자 하는 코드의 키

# 함수 호출
load_and_execute_code_from_json(json_path, key)
"""