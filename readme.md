# このプロジェクト
勉強用として、機械学習アプリを作りました。バックエンドはGoogleCloud上にフロントエンドはFirebaseでホスティングする予定です 音楽雑誌、音楽書籍から文章を抜き出し、前処理後、WordEmbeddingを実装したライブラリで学習し、アーティストの近傍探索ができるアプリとなります。 このレポジトリはバックエンドのプロジェクトとなります。

# 利用技術一覧
!["Python badge"](https://img.shields.io/badge/-Python-a.svg?logo=Python&style=flat)
!["GCP badge"](https://img.shields.io/badge/-Google%20Cloud%20Platform-a.svg?logo=google%20cloud&style=flat)
!["Github badge"](https://img.shields.io/badge/-Github-181717.svg?logo=github&style=flat)
!["Neo4j badge"](https://img.shields.io/badge/-Neo4j-a.svg?logo=neo4j&style=flat)
!["Elasticsearch badge"](https://img.shields.io/badge/-Elasticsearch-005571.svg?logo=Elasticsearch&style=flat)
!["Ubuntu badge"](https://img.shields.io/badge/-Ubuntu-E95420.svg?logo=Elasticsearch&style=flat)
# 全体構成図
![deawio](https://github.com/masatoise/api-cloud-run-v2-disp-change_localtest_2_Portfolio/blob/image/backend.backend.drawio.png)
# バックエンドプロジェクト構成
<pre>
ROOT
|
|-app.py ＃Webアプリのメイン部分リクエストを直接受け付ける
│-client_test.py
│-Dockerfile　＃CloudRunというサーバーレス環境でコンテナを実行するための設定ファイル
│-flask_validate.py
│-readme.md
│-requirements.txt　＃ビルドのタイミングでインストールするpythonモジュール一覧
│
├─elasticsearch_model
│  │  emodel.py　＃DBへアクセスするためのコアモジュール
│  │  helper_for_disp.py　＃DBの検索結果をレイアウトに合わせるためのヘルパー
│  │  helper_for_search.py　＃DBの検索をするためのヘルパー
│  │
│  └─__pycache__
│          emodel.cpython-310.pyc
│          emodel.cpython-311.pyc
│          helper_for_disp.cpython-310.pyc
│          helper_for_disp.cpython-311.pyc
│          helper_for_search.cpython-310.pyc
│          helper_for_search.cpython-311.pyc
│
└─neo4j_model
    │  nmodel.py　＃グラフDBへアクセスするためのコアモジュール
    │  urlutil.py　＃DBの検索結果をレイアウトに合わせたりするためのヘルパー
    │
    └─__pycache__
            nmodel.cpython-310.pyc
            nmodel.cpython-311.pyc
            urlutil.cpython-310.pyc
</pre>
