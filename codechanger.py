def prepare_code_for_json(input_path, output_path):
    try:
        # 파일을 읽기 모드로 열기
        with open(input_path, 'r', encoding='utf-8') as file:
            # 모든 줄을 읽기
            lines = file.readlines()
            # 각 줄의 끝에서 불필요한 공백을 제거하지 않고 개행 문자 \n 으로 결합
            single_line = '\\n'.join(line.rstrip('\n') for line in lines)

        # 큰따옴표를 이스케이프 처리
        escaped_line = single_line.replace('"', '\\"')

        # 결과를 출력 파일에 저장
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.write(escaped_line)
    except Exception as e:
        print(f"An error occurred: {e}")

# 예제 사용법
input_path = 'codechange.py'  # 원본 코드 파일
output_path = 'code_single.txt'  # JSON에 저장할 준비가 된 파일

# 함수 호출
prepare_code_for_json(input_path, output_path)