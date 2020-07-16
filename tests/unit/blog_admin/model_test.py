import pytest
from model_bakery import baker

from editor.blog_admin.models import Post as PostModel, Hashtags


# Post model
#####################################

@pytest.mark.django_db
def test_post_model_string(freezer):
    """Test Post model __str__ function.
    
    Freezer is needed because post_date field in Post model
    is set to auto_now_add=True,
    which says that the date is automatically set to now.
    We don't know, how your 'now' looks like.
    """
    expected = "01.01.2020 00:00 - \"New Django version is coming\""
    
    freezer.move_to('2020-01-01 00:00:00')
    post_model = baker.make(
        'Post',
        title='New Django version is coming'
    )

    assert str(post_model) == expected


@pytest.mark.django_db
def test_post_model_get_first_tag_without_prepopulation():
    """Test Post model get_first_tag function."""
    expected = ""

    # Despite setted hashtags, function will return empty value
    # Because hashtag field wasn't prepopulated
    tag_set = baker.prepare(Hashtags, _quantity=3)
    tag_set[0].text = "First tag"
    
    post_model = baker.make(
        PostModel,
        hashtags=tag_set
    )

    assert post_model.get_first_tag() == expected


@pytest.mark.django_db
def test_post_model_get_first_tag_with_prepopulation():
    """Test Post model get_first_tag function."""
    expected = "First tag"

    tag_set = baker.prepare(Hashtags, _quantity=3)
    tag_set[0].text = expected
    
    post_model = baker.make(
        PostModel,
        hashtags=tag_set
    )

    # Adding prepopulated tag list field
    post_model.tags = tag_set

    assert post_model.get_first_tag() == expected


@pytest.mark.django_db
def test_post_model_get_first_tag_no_tags_available():
    """Test Post model get_first_tag function."""
    expected = ""
    
    post_model = baker.make(PostModel)

    # Adding empty tag list
    post_model.tags = []

    assert post_model.get_first_tag() == expected
