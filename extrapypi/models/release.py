from extrapypi.extensions import db
from extrapypi.models.types import UnicodeText


class Release(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(UnicodeText, nullable=False)
    download_url = db.Column(db.String(2048, convert_unicode=True))
    home_page = db.Column(db.String(2048, convert_unicode=True))
    version = db.Column(db.String(80, convert_unicode=True))
    keywords = db.Column(db.String(255, convert_unicode=True))
    md5_digest = db.Column(db.String(32), nullable=False)

    package_id = db.Column(db.Integer, db.ForeignKey('package.id', name='_fk_release_package'), nullable=False)

    package = db.relationship('Package', backref=db.backref('releases', lazy='dynamic'), lazy='joined')

    def __repr__(self):
        return "<Release {version} for package {package.name}>".format(self)
