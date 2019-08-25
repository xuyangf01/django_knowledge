from haystack import indexes
# 引入项目下的model（也就是将其作为检索关键词的models）
from apps.show_idea.models import QuestionCalssTheme


# model名 + Index作为类名
class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # 对问题名、问题内容进行搜索
    qct_name = indexes.CharField(model_attr='qct_name')
    qct_method = indexes.CharField(model_attr='qct_method')

    def get_model(self):
        return QuestionCalssTheme

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(is_show=1)
