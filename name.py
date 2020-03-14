import sys
import random 
import requests
from urllib.parse import quote
from html.parser import HTMLParser
import itertools

FAMILY_NAME = "南"

FAVORITE = '里梨菜温香優希咲花春太陽朱茉莉夫恵柚果実結紀和'

# https://baby.seorgia.net/2018/05/08/nature/
NATURE = "耀秋朝麻旭海丘楓輝影景霞風河木霧桜郷里峻沙宇岳宙天菜苗梨夏波浪西野葉蓮果花羽春火光冬星蛍松岬水湖南嶺柳山柚雪洋陽夜李澪湧梢浬芽渓"

# https://baby.seorgia.net/2018/05/08/health/
HEALTH = "亨憩延健寿成正保永長伸久満康若"

# https://baby.seorgia.net/2018/05/08/happy/
HAPPY = "愛昌晶依潤可賀輝景叶歓貴誼欣慶恋哉倖愉賛幸祝祥好瑞善頼禎尚望泰聖福希満尊耶裕夢良嘉宜喜佳楽朗和嬉壽悦吉"

# https://baby.seorgia.net/2018/05/08/kind/
KIND = "愛渥与厚篤温敦依敬円郁容寛協欽慶佐賛淳惇情仁輔孝暖忠朋丹熱泰密等深護睦恵慈優安靖寧晏柔佑悠侑譲妥予淑朗和縁衛継結"

# https://baby.seorgia.net/2018/05/08/light/
LIGHT = "灯明耀彰昌昭晶朝旭瑛旺鏡輝晃燦晴火光暉星曜陽燈暁"

# https://baby.seorgia.net/2019/01/11/dream/
DREAM = "希夢望志心嘉旺崇成幸未開遊雲海"

# https://baby.seorgia.net/2018/05/08/pretty/
PRETTY = "愛昌絢彩美麗華香郁馨薫京恋咲桜純玉珠那花斐姫眉鞠毬都雅萌佳璃瑠玲環"

# https://baby.seorgia.net/2018/05/08/power/ 
STRENGTH = "威昌荒嵐一延旺丘勝活要完基創巨建洪洸豪盛茂主峻将進碩壮造立平大宇高尭崇隆岳赳猛直恒毅剛貫典天展通虎夏伸昇旗泰初発原火百拓広弘浩武深太兵幹源峰嶺猛山勇揚洋陽凌烈錬剣獅崚起我凜"

# https://baby.seorgia.net/2018/05/08/clever/
CLEVER = "偉著叡英詠覚可学方克儀教訓啓堅憲賢顕才冴貞定悟慧聡諭史知識秀俊章鋭喬卓規整哲徳能矩則範聖宏博敏文法真誠匡理律了倫伶怜玲礼"

# https://baby.seorgia.net/2018/05/08/cool/
COOL = "彰昌旭偉胤瑛英旺鳳輝貴義圭晃志快魁爽栞将章颯翼貫飛流凪光聖星誉誠尊源弥勇凱蘭竜了亮諒凛礼零廉翔雲"

# https://baby.seorgia.net/2019/01/07/%E8%87%AA%E5%88%86%E3%81%AB%E3%80%8C%E8%87%AA%E4%BF%A1%E3%80%8D%E3%81%8C%E6%8C%81%E3%81%A6%E3%82%8B%E6%BC%A2%E5%AD%97/
CONFIDENCE = "信頼偉大海延旺山勝活要完基登巨世法規豪盛茂直峻将進我壮兵立平幹宇高尭崇隆起太百伸典昇"

# https://baby.seorgia.net/2019/01/08/leadership/
LEADERSHIP = "将頼偉主優英旺秀雄徹要貫理揮統幹隆起"

# https://baby.seorgia.net/2018/05/08/rich/
RICH = "潤富満裕豊環栄"

if sys.argv[1] == 'm':
    MALE = True
    # For Boys
    CANDIDATES = "".join([
            STRENGTH,
            CLEVER,
            COOL,
            CONFIDENCE,
            LEADERSHIP,
            RICH
        ])
else:
    MALE = False
    # For Girls
    CANDIDATES = "".join([
            NATURE,
            HEALTH,
            HAPPY,
            KIND,
            LIGHT,
            DREAM,
            PRETTY
        ])


DAIKICHI = "大吉"
KICHI = "吉"
KYO = "凶"

SCORE_DAIKICHI = 3
SCORE_KICHI = 2
SCORE_KYO = -1
SCORE_OTHER = 1

ENAMAE_URL = "https://enamae.net/{}/{}__{}#result"


class EnamaeHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.res_found = False
        self.result = list()

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            for attr in attrs:
                if attr[1] is not None and "res" in attr[1]:
                    self.res_found = True

    def handle_endtag(self, tag):
        self.res_found = False

    def handle_data(self, data):
        if self.res_found:
            self.result.append(data)


for x in itertools.product(FAVORITE, CANDIDATES):
    for y in itertools.permutations(x):
        name = "".join(y)

        html = requests.get(ENAMAE_URL.format("m" if MALE else "f", quote(FAMILY_NAME), quote(name)));
        parser = EnamaeHTMLParser()
        parser.feed(html.text)
        fortune = parser.result

        num_daikichi = fortune.count(DAIKICHI)
        num_kichi = fortune.count(KICHI)
        num_kyo = fortune.count(KYO)
        score = num_daikichi * SCORE_DAIKICHI + num_kichi * SCORE_KICHI + \
                num_kyo * SCORE_KYO + (len(fortune) - num_daikichi - num_kichi - num_kyo) * SCORE_OTHER

        print("{} : {} : {}".format(score, name, str(fortune)))

