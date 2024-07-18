import random

LI = [
   "デラソウル",
"ティンパンアレイ",
"ジョンリーフッカー",
"チャールズミンガス",
"キングギドラ",
"ジャザノバ",
"ロニサイズ",
"レッドツェッペリン",
"カーティスメイフィールド",
"ジョンコルトレーン",
"セシルマクビー",
"カマシワシントン",
"サンダーキャット",
"ティキマン",
"キャンディド",
"マスターズアットワーク",
"ラリーハード",
"マイケルジャクソン",
"ローリンヒル",
"フランクシナトラ",
"エディパルミエリ",
"マッドプロフェッサー",
"エイドリアンシャーウッド",
"オーガスタスパブロ",
"リーペリー"
]

LIMIT = len(LI)

def gen_random_int_no_dup(n=10):
    return random.sample(range(LIMIT),n)

def get_target_artist_list(_artist_li):
    res = []
    for _idxx in _artist_li:
        _artist =  LI[_idxx]
        res.append(_artist)
    return res
