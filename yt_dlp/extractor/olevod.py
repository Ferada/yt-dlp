# -*- mode: python; coding: utf-8 -*-

from __future__ import unicode_literals

from .common import InfoExtractor


class OlevodIE(InfoExtractor):
    _VALID_URL = r'https://olevod\.com/index\.php/vod/play/id/(?P<id>\d+)/sid/(?P<sid>\d+)/nid/(?P<nid>\d+)\.html'
    _TEST = {
        'url': 'https://olevod.com/index.php/vod/play/id/29583/sid/1/nid/1.html',
        'info_dict': {
            'id': '29583/1/1',
            'ext': 'mp4',
            'title': '云南虫谷',
            'description': r're:^网剧《云南虫谷》.+$',
            'thumbnail': '/upload/vod/20210830-1/790c0f03e1711a45a66637f966a94727.jpg'
            # 'duration': 1511,
            # 'timestamp': 1483619655,
            # 'upload_date': '20170105',
            # 'uploader': 'サトTV',
            # 'uploader_id': 'satotv',
            # 'view_count': int,
            # 'comment_count': int,
            # 'is_live': False
        },
        'params': {
            # m3u8 download
            'skip_download': True
        }
    }

    def _real_extract(self, url):
        valid = self._match_valid_url(url)
        video_id = '{}/{}/{}'.format(valid.group('id'), valid.group('sid'), valid.group('nid'))

        webpage = self._download_webpage(url, video_id)

        options = self._parse_json(
            self._search_regex(
                r'player_aaaa\s*=\s*({.+?})\s*</script>',
                webpage, 'initial context'),
            video_id)

        url = options['url']

        formats = self._extract_m3u8_formats(
            url, video_id, 'mp4', 'm3u8_native', m3u8_id='hls')

        title = self._html_search_regex(
            r'<h2 class="title margin_0">(.+?)</h2>', webpage,
            'title', default=None)

        description = self._html_search_regex(
            r'<div class="panel play_content".+?>\s*<p>.+?</p><p>.+?</p><p>(.+?)</p>\s*</div>', webpage,
            'description', default=None)

        thumbnail = self._proto_relative_url(self._search_regex(
            r'<div class="play_vlist_thumb vnow lazyload" data-original="(?P<url>.+?)">',
            webpage, 'thumbnail url', default=None,
            group='url'))

        return {
            'id': video_id,
            'formats': formats,
            'title': title,
            'description': description,
            'thumbnail': thumbnail
        }
