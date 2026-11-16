# LoveStrong 公式サイト

静的なサイトです。Pythonで、HTMLを書き出します。

## 作り直し方
```
python3 src/build_company.py
```
`company-site/dist/` に、公開用のファイルが出来ます。

## 書き換える所（`src/build_company.py`）
- `MAIL` … 問い合わせのメールアドレス（今は仮の `info@example.com`）
- `BASE` … 公開URL（今は仮の `https://example.com`）
- 各ページの文面（トップ、制作内容、ご依頼の流れ、チーム概要）

## 色
`src/company.css` の末尾の `:root` にある `--orange`（赤）などの変数です。

## 公開（Cloudflare Pages）
```
cd company-site
npx wrangler pages deploy dist --project-name <プロジェクト名> --branch main
```
