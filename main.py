import os
import json
import numpy as np
import pandas as pd
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from pixellib.instance import instance_segmentation
import os
import subprocess
import requests


def classidicator(url):
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'

    data = requests.get(url).content

    g = open('img.jpg', 'wb')
    g.write(data)
    g.close()

    def object_detection_on_an_image():
        segment_image = instance_segmentation()
        segment_image.load_model("D:/class/mask_rcnn_coco.h5")

        target_class = segment_image.select_target_classes(BG=True, person=True, bicycle=True, car=True,
                                                           motorcycle=True, airplane=True, bus=True, train=True,
                                                           truck=False, boat=False, traffic_light=False,
                                                           fire_hydrant=False,
                                                           stop_sign=True, parking_meter=True, bench=True, bird=True,
                                                           cat=True,
                                                           dog=True, horse=True, sheep=True, cow=True, elephant=True,
                                                           bear=True,
                                                           zebra=True, giraffe=True, backpack=True, umbrella=True,
                                                           handbag=True,
                                                           tie=True, suitcase=True, frisbee=True, skis=True,
                                                           snowboard=True, sports_ball=True,
                                                           kite=True, baseball_bat=True, baseball_glove=True,
                                                           skateboard=True, surfboard=True,
                                                           tennis_racket=True, bottle=True, wine_glass=True, cup=True,
                                                           fork=True, knife=True,
                                                           spoon=True, bowl=True, banana=True, apple=True,
                                                           sandwich=True, orange=True, broccoli=True,
                                                           carrot=True, hot_dog=True, pizza=True, donut=True, cake=True,
                                                           chair=True, couch=True,
                                                           potted_plant=True, bed=True, dining_table=True, toilet=True,
                                                           tv=True, laptop=True, mouse=True,
                                                           remote=True, keyboard=True, cell_phone=True, microwave=True,
                                                           oven=True, toaster=True, sink=True,
                                                           refrigerator=True, book=True, clock=True, vase=True,
                                                           scissors=True, teddy_bear=True, hair_dryer=True,
                                                           toothbrush=True)

        # target_class = segment_image.select_target_classes(person=True, car = True)

        result = segment_image.segmentImage(
            image_path="in.jpg",
            show_bboxes=True,
            segment_target_classes=target_class,
            # extract_segmented_objects=True,
            # save_extracted_objects=True,
            output_image_name="out.jpg"
        )

        res1 = tuple(map(str, result[0]["rois"]))
        res2 = tuple(map(str, result[0]["class_ids"]))

        res1 = list(result[0]["rois"])
        res2 = list(result[0]["class_ids"])

        res3 = [0] * len(res2)
        res4 = [0] * len(res2)
        for i in range(len(res2)):
            res3[i] = [0] * 5
        for i in range(len(res2)):
            res4[i] = [0] * 3
        for i in range(len(res2)):
            res3[i][0] = res2[i]
            res3[i][1] = res1[i][1]
            res3[i][2] = res1[i][0]
            res3[i][3] = res1[i][3]
            res3[i][4] = res1[i][2]
        print(res3)
        for i in range(len(res2)):
            res4[i][0] = res3[i][0]
            res4[i][1] = (res3[i][1] + res3[i][3]) // 2
            res4[i][2] = (res3[i][2] + res3[i][4]) // 2
        print(res4)

        res1 = tuple(map(str, res3))
        f = open('info.txt', 'w')
        f.write(''.join(res1))
        f.close()

        with open("asset_list.txt", 'w') as file:
            for row in res4:
                s = ",".join(map(str, row))
                file.write(s + '\n')

        arr = np.array(res3)
        arr = arr.astype('int')
        print(type(arr[0][0]))
        # with open("objects.json", "w") as f:
        # json.dump(arr, f)

    def main():
        object_detection_on_an_image()

    if __name__ == '__main__':
        main()


classidicator(url)

#def set_unity_launch_mode(mode):
    unity_exe_path = "D:/unity/2022.3.7f1/Editor/Unity.exe"
    if not os.path.exists(unity_exe_path):
        print("Путь к исполняемому файлу Unity указан неверно или Unity не установлен.")
        return
    config_path = "C:/Users/mefyq/OneDrive/Рабочий стол/First task Unity/.vsconfig"
    if not os.path.exists(config_path):
        print("Путь к файлу конфигурации Unity указан неверно.")
        return
    with open(config_path, "r") as file:
        config = file.read()
        if mode == "play":
            config = config.replace("EditorStartupMode: 0", "EditorStartupMode: 1")
        elif mode == "pause":
            config = config.replace("EditorStartupMode: 0", "EditorStartupMode: 2")
        elif mode == "edit":
            config = config.replace("EditorStartupMode: 0", "EditorStartupMode: 0")
        else:
            print("Указан неправильный режим запуска Unity.")
        return
    with open(config_path, "w") as file:
        file.write(config)
        print("Режим запуска Unity успешно изменен на", mode)

#set_unity_launch_mode("play")
#subprocess.call('D:/class/First task Unity/ended/First task Unity.exe')


