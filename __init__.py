#!/usr/bin/python3

"""
requirements:
    apt install python3-wand

"""
import os
import shutil
import wand.image

class SplitImages():
    def __init__(self, dirs=None):
        self.dirs = dirs
        self.template = ".{num}.{suffix}"
        self.gray_threshold = 255 - 25

    def get_x_to_be_divided(self, filename=None):
        with wand.image.Image(filename=filename) as img:
            img.depth = 8
            x, y = img.size
            wb = img.make_blob(format='GRAY')

        center_x = x // 2
        #print(len(wb), x, y, x*y, center_x)
        whitebelt = [-1, -1]
        for fx in range(center_x, center_x + 50):
            tf = all(i > self.gray_threshold for i in [
                wb[_xy] for _xy in range(fx, x*y, x)])
            if tf:
                if whitebelt[0] < 0:    
                    whitebelt[0] = fx
            else:
                if whitebelt[0] >= 0:
                    whitebelt[1] = fx
                    break
        else:
            if whitebelt[0] >= 0 and whitebelt[1] < 0:
                whitebelt[1] = fx
        #print(fx, whitebelt)
        return int(sum(whitebelt)/2)

    def split_image(self, filename=None):
        suf = filename.split(".")[-1].lower()
        self.template = ".{num}.{suffix}"
        if self.template.format(num=0, suffix=suf) in filename:
            "foo.bar.0.jpg is processed already"
            return None

        if os.path.exists(filename + self.template.format(num=0, suffix=suf)):
            "Already exists"
            return None

        x2bd = self.get_x_to_be_divided(filename)
        if x2bd and x2bd > 1:
            _tf = "wand_tmp_" + self.template.format(num=9, suffix=suf)
            with wand.image.Image(filename=filename) as origin:
                x, y = origin.size
                with origin[x2bd:x, 0:y] as right_img:
                    _fn = filename + self.template.format(num=0, suffix=suf)
                    right_img.save(filename=_tf)
                    self.move(_tf, _fn)
                with origin[0:x2bd, 0:y] as left_img:
                    _fn = filename + self.template.format(num=1, suffix=suf)
                    left_img.save(filename=_tf)
                    self.move(_tf, _fn)
            os.remove(filename)
            return True
        "x -- axis to be devided -- was not found"
        return True

    def move(self, src=None, dst=None):
        try:
            os.rename(src, dst)
        except OSError:
            shutil.copy(src, dst)
            os.remove(src)

    def split_images(self):
        for _d in self.dirs:
            for cd, _, _f in os.walk(_d):
                for _fp in sorted(_f):
                    target = f'{cd}/{_fp}'
                    self.split_image(filename=target)

if __name__ == '__main__':
    _d = SplitImages(["/tmp/foo", "/tmp/bar"])
    _d.split_images()
