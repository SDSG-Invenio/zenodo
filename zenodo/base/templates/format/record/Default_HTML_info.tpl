{%- from "github/helpers.html" import doi_badge with context %}

{{ bfe_openaire_altmetric(bfo, prefix='<div class="well metadata">', suffix="</div>", badgetype='donut', details='left', no_script='1') }}

{% set published_in = record|zenodo_related_links %}

{% if published_in %}
<div class="well metadata">
{% for item in published_in %}
<small class="text-muted">{{item.text}}</small>
<a href="{{item.link}}"><img src="{{ url_for('static', filename=item.image) }}" class="img-thumbnail" width="100%" /></a>{% endfor %}
</div>
{% endif %}

<div class="well metadata">
  <dl>
    {{ bfe_date(bfo, date_format='%d %B %Y', prefix='<dt>Publication date:</dt><dd>', suffix='</dd>') }}
    {% if record.doi %}
    <dt>DOI</dt>
    <dd>{% if record.doi|is_local_doi %}{{doi_badge(record.doi)}}{% else %}{{ record.doi|doi_link }}{% endif %}</dd>
    {% endif%}
    {{ bfe_isbn(bfo, prefix='<dt>ISBN:</dt><dd itemprop="isbn">', suffix='</dd>') }}
    {{ bfe_report_numbers(bfo, prefix='<dt>Report number(s):</dt><dd>', suffix='</dd>') }}
    {{ bfe_dec(bfo, prefix='<dt>DEC:</dt><dd>', suffix='</dd>', keyword_prefix='<span class="label label-default" itemprop="keywords">', keyword_suffix='</span>', separator=' ') }}
    {{ bfe_dei(bfo, prefix='<dt>DEI:</dt><dd>', suffix='</dd>', keyword_prefix='<span class="label label-default" itemprop="keywords">', keyword_suffix='</span>', separator=' ') }}
    {{ bfe_publi_info(bfo, prefix='<dt>Published in:</dt><dd>', suffix='</dd>') }}
    {{ bfe_openaire_published_in_book(bfo, prefix='<dt>Published in:</dt><dd>', suffix='</dd>') }}
    {{ bfe_publisher(bfo, prefix='<dt>Publisher:</dt><dd>', suffix='</dd>') }}
    {{ bfe_place(bfo, prefix='<dd>', suffix='</dd>') }}
    {{ bfe_language(bfo, prefix='<dt>Language:</dt><dd>', suffix='</dd>') }}
    {{ bfe_country(bfo, prefix='<dt>Country:</dt><dd>', suffix='</dd>') }}
    {{ bfe_field(bfo, escape="0", tag="536__a", prefix='<dt>Grants:</dt><dd>', suffix='</dd>', instances_separator='<br />') }}
    {{ bfe_openaire_university(bfo, prefix='<dt>Thesis:</dt><dd>', suffix='</dd>') }}
    {{ bfe_openaire_meeting(bfo, prefix='<dt>Meeting:</dt><dd>', suffix='</dd>') }}
    {{ bfe_pagination(bfo, prefix='<dt>Pages:</dt><dd itemprop="numberOfPages">', suffix='</dd>', default='', escape='') }}
    <dt>INIS volume:</dt>
	<dd>Volume {{bfo.field('888__a')}} - Issue {{bfo.field('888__b')}}</dd>
    {%- for group in record.related_identifiers|groupby('relation') %}
    {%- if loop.first %}<dt>Related publications and datasets:</dt>{% endif %}
        <dd>{{group.grouper|relation_title}}:<br />
    {%- for related_id in group.list %}{% set related_url = related_id|pid_url %}
        {% if related_url %}<a href="{{related_id|pid_url}}">{{related_id.identifier}}</a>{% else %}<i>{{related_id.identifier}}</i> ({{related_id.scheme|upper}}){% endif %}{% if not loop.last %}, {% endif %}
    {%- endfor %}
    {%- endfor %}
    {%- for alternateid in record.alternate_identifiers %}
    {%- set alternate_url = alternateid|pid_url -%}
    {%- if loop.first %}<dt>Alternate identifiers:</dt><dd>{% endif %}
        {%- if alternate_url -%}
            <a href="{{alternate_url}}">{{alternateid.scheme}}:{{alternateid.identifier}}</a>
        {%- else -%}
            {{alternateid.scheme}}:{{alternateid.identifier}}
        {%- endif -%}
    {%- if loop.last %}</dd>{% endif %}
    {%- endfor %}
    {{ bfe_appears_in_collections(bfo, prefix='<dt>Collections:</dt><dd>', suffix='</dd>') }}
    {{ bfe_openaire_license(bfo, prefix='<dt>License (for files):</dt><dd>', suffix='</dd>') }}
    {% if bfo.field('8560_y') %}
    <dt>Uploaded by:</dt>
    <dd><a href="{{ url_for('yourmessages.write', sent_to_user_nicks=bfo.field('8560_y')) }}">{{bfo.field('8560_y').decode('utf8')}}</a> (on {{ bfe_creation_date(bfo, date_format="%d %M %Y") }})</dd>
    {% else %}
    <dt>Uploaded on:</dt>
    <dd>{{ bfe_creation_date(bfo, date_format="%d %M %Y") }}</dd>
    {% endif %}
  </dl>
</div>
