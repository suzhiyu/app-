from App.Driver import Driver


class DiscoverPage:

    @property
    def shopping_view(self):
        return Driver.d(resourceId="com.nonoapp:id/imageView2")

    @property
    def community_view(self):
        return Driver.d(resourceId="com.nonoapp:id/view_community")

    @property
    def mission_view(self):
        return Driver.d(resourceId="com.nonoapp:id/tv_my_task")

    @property
    def company_introduce_view(self):
        return Driver.d(resourceId="com.nonoapp:id/tv_find_gallery_text")

    @property
    def safe_view(self):
        return Driver.d(resourceId="com.nonoapp:id/tv_find_gallery_text", text=u"省心出借")

    @property
    def new_users_guidance_view(self):
        return Driver.d(resourceId="com.nonoapp:id/tv_find_gallery_text")

    @property
    def sign_in_view(self):
        return Driver.d(text='每日签到')

    @property
    def activity_center_view(self):
        return Driver.d(text='活动中心')

    @property
    def invite_friends_view(self):
        return Driver.d(text='邀请好友')

