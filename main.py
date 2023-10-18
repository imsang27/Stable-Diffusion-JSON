import os
import json

# 경로 설정
paths = [
    os.path.expanduser("C:\\stable-diffusion-webui\\models\\Stable-diffusion"),  # Model
    os.path.expanduser("C:\\stable-diffusion-webui\\models\\Lora"),  # LoRA
    os.path.expanduser("C:\\stable-diffusion-webui\\extensions"),  # Extensions
]

# 가져올 확장자 목록 설정
target_extensions = tuple(["safetensors", "checkpoint", "ckpt"])  # 튜플로 변환

# 모든 경로에서 파일 목록을 저장할 딕셔너리
file_dict = {}

# 예외 처리 추가
try:
    # 모든 경로의 하위 파일 가져오기
    for path in paths:
        if path != os.path.expanduser("C:\\stable-diffusion-webui\\extensions"):  # 특정 경로 제외
            folder_files = {}
            for root, dirs, files in os.walk(path):
                for file_name in files:
                    if file_name.endswith(target_extensions):  # 튜플 사용
                        relative_path = os.path.relpath(root, path)
                        if relative_path == '.':  # 현재 디렉토리를 나타내는 '.' 문자 확인
                            folder_structure = []  # 빈 리스트 사용하여 현재 디렉토리 표현 제거
                        else:
                            folder_structure = relative_path.split(os.sep)
                        current_level = folder_files
                        for folder in folder_structure[:-1]:  # 마지막 폴더를 제외하고 순회
                            current_level = current_level.setdefault(folder, {})
                        # 마지막 폴더를 키로 사용하고 파일 이름의 리스트를 값으로 사용
                        if folder_structure:  # folder_structure가 비어 있지 않은 경우에만 액세스
                            current_level.setdefault(folder_structure[-1], []).append(file_name)

            # 폴더 이름 추가 (폴더 이름은 해당 경로의 마지막 부분입니다)
            folder_name = os.path.basename(path)
            if folder_name != "extensions":
                file_dict[folder_name] = folder_files

    # Extensions 경로의 폴더 이름을 "extensions" 배열에 추가
    extensions_path = os.path.expanduser("C:\\stable-diffusion-webui\\extensions")  # 중복 제거
    extensions_folders = [folder_name for folder_name in os.listdir(extensions_path) if os.path.isdir(os.path.join(extensions_path, folder_name))]
    file_dict["extensions"] = extensions_folders

except Exception as e:
    print(f"Error: {e}")  # 오류 메시지 출력

# JSON 파일에 저장
output_file = "Stable_Diffusion.json"  # 저장할 JSON 파일 이름
with open(output_file, "w", encoding='utf-8') as json_file:  # 인코딩 추가
    json.dump(file_dict, json_file, indent=4, ensure_ascii=False)  # indent와 ensure_ascii 옵션 사용

print(f"선택된 파일 목록을 '{output_file}'로 저장하였습니다.")