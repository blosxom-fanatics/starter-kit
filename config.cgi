# blosxom設定ファイル ==================================================

# blosxomをUTF-8やEUC-JPなどで利用する場合は、このファイルもそれぞれの文
# 字コードにあわせる必要があります。

# 主な設定 =============================================================

# blogのタイトル
$blog_title = "blosxom starter kit";

# blogの説明
$blog_description = "blosxomで今すぐできるウェブログ・キット";

# blogの言語
$blog_language = "ja";

# blosxom本体の設定 ====================================================

# blosxomを設置したディレクトリ
$basedir = "/virtual/foo/public_html/blosxom";

# エントリを置くディレクトリの絶対パス
$datadir = "$basedir/entries";

# blosxomを設置したURL
# 空欄にすると自動的に取得します
$url = "http://example.com/blosxom/blosxom.cgi";

# エントリを探すためにエントリを置くディレクトリより辿る階層数
# 0: 全て辿る
# 1: エントリを置くディレクトリのみ
# n: n階層辿る
$depth = 0;

# 1ページに表示するエントリの数
$num_entries = 15;

# エントリとみなすファイルの拡張子
$file_extension = "txt";

# デフォルトのフレーバー名
$default_flavour = "html";

# 未来の日付けのエントリを表示するかどうか
# 0: 表示しない
# 1: 表示する
$show_future_entries = 0;

# プラグイン関連の設定 =================================================

# プラグインを置くディレクトリの絶対パス
$plugin_dir = "$basedir/plugins";

# プラグインの各種情報を置くディレクトリの*サーバー上での*絶対パス
$plugin_state_dir = "$plugin_dir/states";

# 静的生成関連の設定 ===================================================

# 静的生成したファイルの出力先の絶対パス
$static_dir = "$basedir/statics";

# 静的生成するときに必要なパスワード(静的生成を利用する場合は必須)
$static_password = "";

# 生成するフレーバー名(半角スペースで区切って、複数指定可能)
@static_flavours = qw/html rss/;

# Should I statically generate individual entries?
# 0: 生成しない
# 1: 生成する
$static_entries = 0;

# 各プラグインの設定 ===================================================

# archives ----------------------------------------

# 月の並び順の設定
# 0: 古い方が上
# 1: 新しい方が上
$archives_reverse = 1;

# インデントに使う文字列(\tなど)
$archives_indent = "";

# 月の表示に使う文字列
@archives_monthname = (
  "一月",
  "二月",
  "三月",
  "四月",
  "五月",
  "六月",
  "七月",
  "八月",
  "九月",
  "十月",
  "十一月",
  "十二月",
);

# bookmarklet ----------------------------------

# TrackBack ping URLを探すかどうか
# LWP::Simpleモジュールが必要です
# 0: 探さない
# 1: 探す
$bookmarklet_trackback_discovery = 0;

# categories -----------------------------------

# エントリ数の表示に子カテゴリのエントリの数も含めるかどうか
# 0: 含めない
# 1: 含める
$categories_story_count_commulative = 1;

# 出力形式
# ul: UL
# m4: 謎すぎ
$categories_output_format = 'ul';

# 最上位カテゴリ名
$categories_root_name = "全てのエントリ";

# 除外するカテゴリ
# "/foo"を指定した場合、"/foo/bar"や"/foo/hoge"などは除外されますが、
# "/foo"自体は除外されません
# 半角スペースで区切って複数指定可能
@categories_prune_dirs = qw(/old /draft);

# カテゴリの別名
%categories_aliases = (
  'plugins' => 'プラグイン',
  'weblog'  => 'ウェブログ',
  'news'    => 'ニュース',
);

# カテゴリ同士の間に入れる文字列
$categories_sep = "::";

# css ------------------------------------------

# "http://"または"/"で始まるCSSファイルの絶対URL
# 複数指定すると、アクセスごとにランダムに切り替わります
@css_paths = (
  "http://example.com/blosxom/style-sites.css",
);

# date_title -----------------------------------

# blogのタイトルと年月日の間に入れる文字列
$date_title_title_sep = ' :: ';

# 年と月、月と日の間に入れる文字列
$date_title_date_sep = '/';

# entry_index ----------------------------------

# データを格納するファイル名
$entries_index_datafile = "$plugin_state_dir/entries_index.dat";

# entry_title ----------------------------------

# blogのタイトルとエントリのタイトルの間に入れる文字列
$entry_title_title_sep = ' :: ';

# google ---------------------------------------
# URI::Escapeモジュールが必要です

# Googleでの検索結果にリダイレクトするCGIの絶対URLまたは"/"で始まる絶対パス
$google_cgi_path = "/blosxom/google.cgi";

# 検索結果を絞り込むためのキーワード
# site:example.com
# inurl:example.org/~yourname/ $blog_title
# などうまく指定してやってください
$google_keyword = "site:example.com";

# rss10 ----------------------------------------

# 名前
$rss10::creator = 'John Doe';

# メールアドレス
$rss10::email = 'john-doe@example.com';

# 時差(日本の場合は+9:00です)
$rss10::tz_offset = '+09:00';

# wikieditish ----------------------------------

# エントリファイルの更新時刻を保持する
# OSによっては意味がないかもしれません
# 0: 保持しない
# 1: 保持する
$wikieditish_preserve_lastmodified = 0;

# エントリの編集にパスワードを必要とする
# 0: 必要としない
# 1: 必要とする
$wikieditish_require_password = 1;

# パスワード(必須)
$wikieditish_blog_password = "";

# 編集を許可するIPアドレスを制限する
# 0: 制限しない
# 1: 制限する
$wikieditish_restrict_by_ip = 0;

# 許可するIPアドレス
# 半角スペースで区切って複数指定可能
@wikieditish_ips = qw(127.0.0.1 192.168.0.1);

# 編集後のエントリの拡張子
# 場合によっては必要とするかもしれないですが・・・
$wikieditish_file_extension = $blosxom::file_extension;

# 編集と同時にTrackBackを送信する
# LWP::UserAgentモジュールとHTTP::Request::Commonモジュールが必要です。
# 0: 送信しない
# 1: 送信する
$wikieditish_send_pings = 0;

# TrackBackの文字コード
# UTF-8:       UTF-8
# Shift_JIS:   Shift_JIS
# EUC-JP:      EUC-JP
# ISO-2022-JP: ISO-2022-JP
$wikieditish_tb_charset = "UTF-8";

# writeback ------------------------------------

# writebackのデータを保存するディレクトリ名
$writeback_dir = "$plugin_state_dir/writebacks";

# writebackのデータファイルの拡張子
# blosxomのエントリファイルの拡張子とは違うものを指定
$writeback_file_extension = "wb";

# writebackのパラメータ
# 半角スペースで区切って複数指定可能
@writeback_fields = qw(title name blog_name url comment excerpt);

# 不正なヘッダと共に投稿されたコメントを拒否する
# 0: 拒否しない
# 1: 拒否する
$writeback_block_invalid_header_cm = 0;

# 不正なヘッダと共に投稿されたTrackBackを拒否する
# 0: 拒否しない
# 1: 拒否する
$writeback_block_invalid_header_tb = 0;

# ASCIIのみのコメントまたはTrackBackを拒否する
# 0: 拒否しない
# 1: 拒否する
$writeback_block_ascii_only = 1;

# 送られてきたTrackBackの文字コードを変換する
# Jcodeモジュールが必要です
# 0: 変換しない
# 1: 変換する
$writeback_conv_charset = 0;

# 文字コード
# utf8: UTF-8
# sjis: Shift_JIS
# euc:  EUC-JP
# jis:  JIS
$writeback_charset = 'utf8';

# クッキーを割り当てるドメイン
$writeback_cookie_domain = ".example.com";

# クッキーを割り当てるパス
$writeback_cookie_path = "/blosxom";

# クッキーの有効期限
$writeback_cookie_expires = "+3M";

# コメントまたはTrackBackがあった時にメールで通知
# Jcodeモジュールが必要です
# 0: メールで通知しない
# 1: メールで通知する
$writeback_notify_mail = 0;

# sendmailのパス
$writeback_sendmail = '/usr/local/bin/sendmail';

# Fromヘッダに使用するメールアドレス
$writeback_from = 'john-doe@example.com';

# Toヘッダに使用するメールアドレス
$writeback_to = 'john-doe@example.com';

# ----------------------------------------------------------------------

1;
