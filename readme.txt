blosxom starter kit
------------------------------------------------------------------------

■ はじめに

blosxom starter kitは、blosxom本体といくつかのplugin、デザインを決定する
flavourをまとめたものです。基本的には、設定ファイル(config.cgi)を設置す
るサーバーに合わせて編集し、ファイルやディレクトリのパーミッションをそれ
ぞれきっちりと設定してやるだけで、blosxomでblogをはじめることが出来ると
いうことになります。

blosxom starter kitに関して、blosxomの作者であるRael Donfestさんには許可
は貰いましたが、彼とblosxom starter kitには、直接的には何も関係がありま
せん。ゆえに、blosxom starter kitに関する問い合わせは、必ず制作者である
私(kyo@hail2u.net)にお願いします。

また、あなたがblosxom starter kitを利用したことによって、何らかの不利益
をこうむったとしても、blosxom作者であるRael Donfestさんはもちろん、この
blosxom starter kitの制作者である私も関知しません。

■ ライセンス

基本的にblosxomのライセンスに従います。blosxom starter kitにおいて、特別
に加わる制限その他はありません。

Licsense

Blosxom
Copyright 2003, Rael Dornfest

blosxom starter kit
Copyright 2004, Kyo Nagashima

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the
following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


■ 同梱ファイル・ディレクトリ

blosxom.cgi
  blosxom本体のCGIスクリプトです。設定を外部ファイルから読み込むように改
  造してあります。

chkfullpath.cgi
  簡易フルパスチェック用のCGIスクリプトです。

config.cgi
  blosxom starter kitの設定ファイルです。このファイルにblosxom本体、及び
  同梱しているplugin全ての設定があります。

google.cgi
  Googleでサイト内検索を行った結果のページにリダイレクトするCGIスクリプ
  トです。同梱しているgoogleというblosxomのプラグインと連携して動作する
  ので、特に編集する必要はありません。

style-sites.css
  Movable Typeの配布サイトで配布されているStormyという名のCSSファイルに
  大幅に手を加えたものです。blosxom starter kitが生成するHTMLは、Movable
  Typeがデフォルトで生成するHTMLと互換性がありますので、いろいろなサイト
  で配布されているMovable Typeのデフォルト・テンプレートに利用することが
  できるCSSファイルをそのまま流用できます。

entriesディレクトリ
  blosxomのflavour及びエントリを格納している(格納する)ディレクトリです。
  同梱しているflavourは、設置するサーバーに依存しないように作成してある
  ので、そのまま使う場合は特に編集する必要はありません。

pluginsディレクトリ
  blosxomのpluginを格納しているディレクトリです。blosxom starter kitに同
  梱しているpluginに限っては、全ての設定をconfig.cgiに移動してあるので、
  そのまま使う場合は、特に編集する必要はありません。


■ 設定

blosxom.cgi及びchkfullpath.cgi、google.cgi
  一行目のPerlのパスを、設置するサーバーに合わせて書き換えてください。

config.cgi
  それぞれの設定を、設置するサーバーや好みに合わせて編集してください。簡
  単な説明がコメントとして付記してありますので、それを参照しながらひとつ
  ひとつきちんと設定してください。同梱のabout_config.txtに個々の設定につ
  いて詳しく書いておきましたので、そちらも良くお読みください。


■ 転送及びパーミッションの設定

blosxom starter kitのアーカイブを展開したままのディレクトリ構造で転送し
てください。このディレクトリ構造が崩れてしまうと、正常に動作しない可能性
が高いです。FTPアプリケーションのミラーリング・アップロードなどの機能を
利用すると良いかと思います。

パーミッションの設定が必要なのは以下のファイル及びディレクトリです。

  blosxom.cgi                755
  chkenv.cgi                 755
  chkfullpath.cgi            755
  google.cgi                 755
  entriesディレクトリ        777
    first_post.txt           666
  pluginsディレクトリ        変更の必要はありません
    statesディレクトリ       777

かなり煩雑ですが、blosxomが読み書きできるようにパーミッションを与えてや
らないとならないので、きちんと設定してあげてください。suExecなどを利用し
ているサーバーの場合は、もっと厳しいパーミッションでも動作することと思い
ますが、それについてはご自身でお調べください。


■ blosxomでblog

きちんと設定、転送、パーミッションの設定を終え、ブラウザでblosxom.cgiに
アクセスすると、first_post.txtの内容が表示されることと思います。あとは好
きなようにエントリを書いていくだけです。同梱してある最初のエントリが邪魔
な場合は、FTPでfirst_post.txtをentriesディレクトリから削除してください。

エントリの作成やカテゴリの作成はblosxom本家のサイト、もしくはそれの日本
語に訳したblosxomサイトの日本語訳を参照してください。

  blosxom                 http://www.blosxom.com/
  blosxomサイトの日本語訳 http://www.yk.rim.or.jp/%7Esucle/blosxom/

エントリの編集にはwikieditishというプラグインを使用しています。エントリ
の新規作成にこれを利用することも可能です。例えば、「hogehoge.txt」という
ファイル名で新たにエントリを作成したい場合は、

  http://example.com/blog/blosxom.cgi/hogehoge.wikieditish

というアドレスをブラウザで開くと、何も入力されていないフォームが表示され
るので、そこでタイトルと本文を記入しPostボタンを押せばエントリが作成され
ます。また、新たにカテゴリを作成した上でエントリを作成したい場合、例えば、
「hoge」というカテゴリに「hage.txt」というファイル名で新たにエントリを作
成したい場合は、

  http://example.com/blog/blosxom.cgi/hoge/hage.wikieditish

というアドレスをブラウザで開くことになります。

基本的な使い方は以上です。使い方には色々と注意すべき点があるのですが、到
底全てについて書くことは出来ないので、詳しくはインターネットを検索するな
りして、ご自身で解決してください。色々と検索してみた後に、どうしてもわか
らないことがある時は、何がどうわからないのかをはっきりとさせた上で、それ
をきちんとまとめた

  * メールをkyo@hail2u.net宛てに送る
  * コメント(またはTrackBack)をhttp://hail2u.net/blog/のblosxom starter
    kitに関するエントリへ投稿
  * コメントをhttp://hail2u.net/bbs/へ投稿

以上3つのいずれかの手段で質問してください。出来うる限り対処させていただ
きますが、場合によっては無視することもあるかもしれません。なお、繰り返し
になりますが、このblosxom starter kitを使用した場合は、blosxom作者のRael
Donfestさんや個々のプラグイン作者の方々には聞かないでください。


■ 補足

blosxom starter kitはあらかじめいくつかのpluginやflavourを同梱しています
が、blosxomの動作自体には何も手を加えていませんので、公式サイトやその他
いろいろな場所で配布されているpluginやflavourを利用することに問題はあり
ません。しかしながらplugin同士の相性の問題などが少なからず存在します。そ
の辺りの事情については関知できませんのでご容赦ください。また、それらの同
梱されていないpluginやflavourの導入に関してもサポートできません。


■ 更新履歴

2005/02/23 1.1.3

  * writebackで生成されるa要素のrel属性の値に"nofollow"を指定するように
    した
  * wikieditishが正常に設定を読み込んでいない不具合を修正した

2004/08/13 1.1.2

  * foot.wikieditishのマークアップのミスを修正した
  * JavaScriptによるwikieditishでのプレビュー機能を追加した
  * writebackのコードを一部変更した

2004/08/13 1.1.1

  * wikieditishのTrackBack送信機能のバグを修正した

2004/08/12 1.1

  * wikieditishのメッセージを多少わかりやすくした
  * wikieditishのTrackBack送信機能で、タイトルにHTMLタグが含まれている場
    合に削除する処理を追加した
  * writebackにコメント・スパムへの対策を追加した
  * writebackのデータファイルにリモート・ホストとリモート・アドレスを記
    録するようにした
  * wikieditishのTrackBack送信機能で、パラメータとして送信する文字コード
    の設定を追加した
  * writebackのスパム対策の有効・無効を切り替える設定を追加した

2004/08/07 1.0.3

  * writebackの任意のJavaScriptコードを実行される脆弱性に対処をした

2004/08/07 1.0.2

  * writebackのTrackBackをSPAMに悪用される脆弱性に部分的な対処をした

2004/07/01 1.0.1a

  * flavourでのつづり間違いを修正した

2004/06/23 1.0.1
  * flavour(foot.htmlとfoot.htm、foot.wikieditish)にblosxom starter kit
    を利用していることを示すリンクを追加した(削除可能)
  * writebackで改行をbr要素に変換するようにした


2004/04/17 1.0
  Initial release


■ 謝辞その他

  blosxom公式サイト       http://www.blosxom.com/
  blosxomサイトの日本語訳 http://www.yk.rim.or.jp/%7Esucle/blosxom/

  plugins
    archives        http://akins.org/blog/
    bookmarklet     http://blog.bulknews.net/
    categories      http://molelog.molehill.org/
    entries_index   http://www.blosxom.com/
    rss10           http://www.blosxom.com/
    wikieditish     http://www.blosxom.com/
    writeback       http://www.blosxom.com/


■ 制作者

  Kyo Nagashima <kyo@hail2u.net>, http://hail2u.net/


------------------------------------------------------------------------
                                                        End of Documents
