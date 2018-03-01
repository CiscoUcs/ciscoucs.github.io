# Document Deployment

To update these docs and deploy them to production run:

```
gitbook build
./deploy.py
git add .
git commit -am "updates"
git push
```