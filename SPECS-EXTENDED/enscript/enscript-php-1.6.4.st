/**
 * Name: php
 * Description: PHP programming language.
 *
 * Author: Daniel Frederiksen, cyberdoc@cyberdoc.dk
 * Extenden functions definition including all PHP functions.
 * 
 * Based on the initial file by 
 * Ian Berry, iberry@raxnet.net. 
 * http://home.raxnet.net/article_viewcvs_php.php

 */
 
state php_comment
{
  /\*\\\// {
    language_print ($0);
    return;
  }
  LANGUAGE_SPECIALS {
   language_print ($0);
  }
}

state php_dquot_string
{
  /\\\\./ {
    language_print ($0);
  }
  /\"/ {
    language_print ($0);
    return;
  }
  LANGUAGE_SPECIALS {
    language_print ($0);
  }
}

state php_quot_string
{
  /\\\\./ {
    language_print ($0);
  }
  /[\']/ {
    language_print ($0);
    return;
  }
  LANGUAGE_SPECIALS {
    language_print ($0);
  }
}

state php_bquot_string
{
  /\\\\./ {
    language_print ($0);
  }
  /`/ {
    language_print ($0);
    return;
  }
  LANGUAGE_SPECIALS {
    language_print ($0);
  }
}

state php
{
  BEGIN {
    header ();
  }
  END {
    trailer ();
  }

  /* Comments. */
  /\/\*/ {
    comment_face (true);
    language_print ($0);
    call (php_comment);
    comment_face (false);
  }
  /\/\// {
    comment_face (true);
    language_print ($0);
    call (eat_one_line);
    comment_face (false);
  }

  /* Ignore escaped quote marks */
  /\\\"/ {
    language_print ($0);
  }
  /\\\'/ {
    language_print ($0);
  }
  /\\\`/ {
    language_print ($0);
  }

  /* stuff after a -> is a method,
   * don't bold just because it looks like a keyword
   */
  /->\w+/ {
    language_print ($0);
  }

  /* stuff between a - and a => is a named parameter,
   * don't bold just because it looks like a keyword
   */
  /-\w+=>/ {
    language_print ($0);
  }

  /* Ignore embedded comments */
  /\/\// {
    language_print ($0);
    call (eat_one_line);
  }

  /* Control flow */
  /(<\?|\?>)/ {
    reference_face (true);
    language_print ($0);
    reference_face (false);
  }

  /* Code control (){} */
  /[\{\}\(\)\[\]]/ {
    reference_face (true);
    language_print ($0);
    reference_face (false);
  }

 /* Numerics & Logics */
  /[\\-+*\/%!`]/ {
    function_name_face (true);
    language_print ($0);
    function_name_face (false);
  }


  /* String constants. */
  /\"/ {
    string_face (true);
    language_print ($0);
    call (php_dquot_string);
    string_face (false);
  }

  /[\']/ {
    string_face (true);
    language_print ($0);
    call (php_quot_string);
    string_face (false);
  }

  /* Backquoted command string */
  /`/ {
    string_face (true);
    language_print ($0);
    call (php_bquot_string);
    string_face (false);
  }

  /* Variables */
  /(\$+[a-zA-Z0-9_-]*)/ {
    variable_name_face (true);
    language_print ($1);
    variable_name_face (false);
  }

  /* Functions (All PHP function 2004-09-19) */
  /\b(a(cosh?|ddc?slashes|ggregat(e(_(methods(_by_(list|regexp))?|properties(_by_(list|regexp))?|info))?|ion_info)|pache_(get(_(modules|version)|env)|re(quest|sponse)_headers|(child_termina|no)te|lookup_uri|setenv)|r(ray(_(c(h(ange_key_case|unk)|o(mbine|unt_values))|diff(_(u(assoc|key)|assoc|key))?|f(il(l|ter)|lip)|intersect(_(u(assoc|key)|assoc|key))?|key(_exist)?s|m(erge(_recursive)?|ap|ultisort)|p(ad|op|ush)|r(e(duc|vers)e|and)|s(earch|hift|p?lice|um)|u(diff(_u?assoc)?|intersect(_u?assoc)?|n(ique|shift))|walk(_recursive)?|values)|iterator_((curren|nex)t|key|(rewin|vali)d|seek)|object_(co(nstruc|un)t|offset(exists|(g|(un)?s)et)|append|getiterator))?|sort)|s(inh?|pell_(check(_raw)?|new|suggest)|sert(_options)?|cii2ebcdic|ort)|tan[2h]?|bs)|b(ase(64_(de|en)code|_convert|name)|c(m(od|ul)|pow(mod)?|s(cale|qrt|ub)|add|comp|div)|in(d(_textdomain_codeset|ec|textdomain)|2hex)|z(c(lose|ompress)|err(no|(o|st)r)|decompress|flush|open|read|write))|c(a(ching(iterator_((has)?next|(rewin|vali)d|tostring)|recursiveiterator_(get|has)children)|l(_(days_in_month|(from|to)_jd|info)|l_user_(func(_array)?|method(_array)?)))|cvs_(a(dd|uth)|co(mmand|unt)|d(elet|on)e|re(port|turn|verse)|s(ale|tatus)|init|lookup|new|textvalue|void)|h(eckd(ate|nsrr)|o(p|wn)|r(oot)?|dir|grp|mod|unk_split)|l(ass(kit_method_(re(defin|mov|nam)e|add|copy)|_exists)|ose(dir|log)|earstatcache)|o(m(_(get(_active_object)?|i(nvoke|senum)|load(_typelib)?|pr(op([gs]e|pu)t|int_typeinfo)|addref|create_guid|event_sink|message_pump|release|set)|pact)?|n(nection_(aborted|status|timeout)|vert_(uu(de|en)code|cyr_string)|stant)|sh?|unt(_chars)?|py)|pdf_(a(dd_(annotation|outline)|rc)|c(l(ose(path(_(fill_)?stroke)?)?|ip)|ircle|ontinue_text|urveto)|fi(ll(_stroke)?|nalize(_page)?)|o(pen|utput_buffer)|p(age_init|lace_inline_image)|r(e(ct|store)|otate(_text)?|(lin|mov)eto)|s(ave(_to_file)?|et(_(c(har_spacing|reator|urrent_page)|font(_(directories|map_file))?|t(ext_(r(endering|ise)|matrix|pos)|itle)|action_url|(horiz_scal|lead|word_spac)ing|(keyword|viewer_preference)s|page_animation|subject)|gray(_(fill|stroke))?|line(cap|join|width)|rgbcolor(_(fill|stroke))?|dash|(fla|miterlimi)t)|how(_xy)?|tr(ingwidth|oke)|cale)|t(ext|ranslate)|(begin|end)_text|global_set_document_limits|import_jpeg|(lin|mov)eto|newpath)|r(ack_(c(heck|losedict)|getlastmessage|opendict)|c32|eate_function|ypt)|type_(al(num|pha)|p(rin|unc)t|cntrl|x?digit|graph|(low|upp)er|space)|ur(l_(c(los|opy_handl)e|e(rr(no|or)|xec)|multi_(in(fo_read|it)|((add|remove)_handl|clos)e|exec|(getconten|selec)t)|getinfo|(ini|setop)t|version)|rent)|y(bercash_(base64_(de|en)code|(de|en)cr)|rus_(c(lose|onnect)|authenticate|(un)?bind|query))|eil)|d(b(a(_(f(etch|irstkey)|op(en|timize)|(clos|delet|replac)e|(exist|handler)s|(inser|key_spli|lis)t|nextkey|popen|sync)|se_(c(los|reat)e|get_(record(_with_names)?|header_info)|num(fiel|recor)ds|(add|(delet|replac)e)_record|open|pack))|m(f(etch|irstkey)|(clos|delet|replac)e|exists|insert|nextkey|open)|plus_(a(dd|ql)|c((hdi|ur)r|lose)|err(code|no)|f(i(nd|rst)|ree((all|r)locks|lock)|lush)|get(lock|unique)|l(ast|ockrel)|r(c(r(t(exact|like)|eate)|hperm)|es(olve|torepos)|keys|open|query|rename|secindex|unlink|zap)|s(etindex(bynumber)?|avepos|ql)|t(cl|remove)|u(n(do(prepare)?|lockrel|select)|pdate)|x(un)?lockrel|info|next|open|prev)|x_(c(o(mpare|nnect)|lose)|e(rror|scape_string)|fetch_row|query|sort)|list)|cn?gettext|e(bug(_(print_)?backtrace|ger_o(ff|n))|c(bin|hex|oct)|fine(_syslog_variables|d)?|(aggrega|le)te|g2rad)|i(o_(s(eek|tat)|t(csetattr|runcate)|(clos|writ)e|fcntl|open|read)|r(ectoryiterator_(c(onstruc|urren)t|file(([acm]tim|inod|siz|typ)e|group|owner|perms)|get(path(name)?|children|filename)|is(d(ir|ot)|(((execu|wri)t|read)ab|fi)le|link)|key|next|(rewin|vali)d)|name)?|sk(_(free|total)_space|freespace)|e)|n(s_(get_(mx|record)|check_record)|gettext)|o(m(_(dom(characterdata_(append|(delet|replac)e|insert|substring)data|document_(create(attribute(ns)?|c(datasection|omment)|e(lement(ns)?|ntityreference)|documentfragment|processinginstruction|textnode)|getelement(sbytagname(ns)?|byid)|load(html(file)?|xml)?|relaxngvalidate(source)?|s(ave(html(file)?|xml)?|chemavalidate(source)?)|((importno|xinclu)d|normaliz|validat)e)|element_(get(attribute(n(ode(ns)?|s))?|elementsbytagname(ns)?)|hasattribute(ns)?|removeattribute(n(ode|s))?|setattribute(n(ode(ns)?|s))?)|implementation_(createdocument(type)?|hasfeature)|n(amednodemap_(getnameditem(ns)?|item)|ode(_(has(attribut|childnod)es|i(ss(amenode|upported)|nsertbefore)|lookup(namespaceuri|prefix)|re(mov|plac)echild|appendchild|(clonenod|normaliz)e)|list_item))|text_(iswhitespaceinelementconten|splittex)t|xpath_(query|registernamespace)|attr_isid)|import_simplexml)|attribute_((nam|valu)e|specified)|document(_(create_(c(data_section|omment)|e(lement(_ns)?|ntity_reference)|(attribut|text_nod)e|processing_instruction)|d(oc(type|ument_element)|ump_(file|mem))|get_element(_by_id|s_by_tagname)|add_root|html_dump_mem|xinclude)|type_(n(ame|otations)|entities|internal_subset|(public|system)_id))|element_(get_(attribute(_node)?|elements_by_tagname)|((has|remove|set)_attribut|tagnam)e)|node_(a(ppend_(child|sibling)|dd_namespace|ttributes)|c(hild_nodes|lone_node)|has_(attribut|child_nod)es|i(nsert_befor|s_blank_nod)e|n(ode_(nam|typ|valu)e|ext_sibling)|p(re(fix|vious_sibling)|arent_node)|re(place_(child|node)|move_child)|set_(name(space)?|content)|(dump|unlink)_node|(fir|la)st_child|(get_cont|owner_docum)ent)|processinginstruction_(data|target)|x(ml_(open_(file|mem)|x(slt_stylesheet(_(doc|file))?|mltree)|new_doc|version)|sltstylesheet_(result_dump_(file|mem)|process)))|tnet(_load)?|ubleval)|ate|gettext|l)|e(a(ster_da(te|ys)|ch)|r(eg(i(_replace)?|_replace)?|ror_(lo|reportin)g)|scapeshell(arg|cmd)|x(i(f_(t(agname|humbnail)|imagetype|read_data)|t)|p(lode|m1)?|t(ension_loaded|ract)|ec)|bcdic2ascii|cho|mpty|nd|val|zmlm_hash)|f(am_(c(ancel_monitor|lose)|monitor_(collection|directory|file)|next_event|open|pending|(resume|suspend)_monitor)|bsql_(a(ffected_rows|utocommit)|c(lo(b_siz|s)e|o(mmi|nnec)t|reate_([bc]lo|d)b|hange_user)|d(ata(base(_password)?|_seek)|b_(query|status)|rop_db)|err(no|or)|f(etch_(a(rray|ssoc)|field|lengths|object|row)|ield_(t(abl|yp)e|flags|len|name|seek)|ree_result)|list_(db|field|table)s|n(um_(field|row)s|ext_result)|p(assword|connect)|r(e(ad_[bc]lob|sult)|ollback)|s(e(t_(lob_mode|password|transaction)|lect_db)|t(art|op)_db)|(blob_siz|(host|table|user)nam)e|get_autostart_info|insert_id|query|warnings)|df_(add_(doc_javascript|template)|c(los|reat)e|e(rr(no|or)|num_values)|get_(a(p|ttachment)|f(ile|lags)|v(alue|ersion)|encoding|opt|status)|open(_string)?|s(ave(_string)?|et_(f(ile|lags)|o(n_import_javascri)?pt|s(tatus|ubmit_form_action)|v(alue|ersion)|ap|encoding|javascript_action|target_frame))|header|next_field_name|remove_item)|get(c(sv)?|ss?)|il(e(_(exis|(ge|pu)t_conten)ts|p(ro(_(field(count|(nam|typ)e|width)|r(etrieve|owcount)))?|erms)|([acm]tim|inod|siz|typ)e|group|owner)?|teriterator_((curren|nex)t|getinneriterator|key|(rewin|vali)d))|l(o(atval|ck|or)|ush)|p(assthru|rintf|uts)|r(e(a|nchtoj)d|ibidi_log2vis)|s(canf|eek|ockopen|tat)|t(p_(c(h(dir|mod)|dup|lose|onnect)|f(ge|pu)t|get(_option)?|m(dtm|kdir)|n(b_(f(ge|pu)t|continue|(ge|pu)t)|list)|p(asv|ut|wd)|r(aw(list)?|ename|mdir)|s(i[tz]e|et_option|sl_connect|ystype)|(allo|exe)c|delete|login|quit)|ell|ok|runcate)|unc(_(get_args?|num_args)|tion_exists)|(clos|writ)e|eof|(flus|nmatc)h|mod|open)|g(et(_(c(lass(_(method|var)s)?|(fg_va|urrent_use)r)|de(clared_(class|interfac)es|fined_(constant|function|var)s)|h(eaders|tml_translation_table)|include(_path|d_files)|m(agic_quotes_(gpc|runtime)|eta_tags)|re(quired_files|source_type)|browser|(extension_func|loaded_extension|object_var|parent_clas)s)|hostby(namel?|addr)|m(y([gpu]id|inode)|xrr)|protobyn(ame|umber)|r(andmax|usage)|servby(name|port)|t(ext|imeofday|ype)|allheaders|(cw|lastmo)d|(dat|imagesiz)e|env|opt)|m(p_(a(bs|[dn]d)|c(lrbit|mp|om)|div(_(qr?|r)|exact)?|gcd(ext)?|in((i|ver)t|tval)|m(od|ul)|p(o(wm?|pcount)|(erfect_squar|rob_prim)e)|s(can[01]|qrt(rem)?|etbit|ign|trval|ub)|(fac|hamdis)t|jacobi|legendre|neg|x?or|random)|(dat|(mk|strf)tim)e)|z(c(lose|ompress)|e(ncode|of)|get(ss?|c)|p(assthru|uts)|re(a|win)d|(((de|in)fla|wri)t|fil)e|open|seek|tell|uncompress)|d_info|lob|regoriantojd)|h(e(ader(s_(lis|sen)t)?|brevc?|xdec)|ighlight_(file|string)|t(ml(_entity_decode|(entitie|specialchar)s)|tp_build_query)|w(_(c(h(ildren(obj)?|angeobject)|onnect(ion_info)?|lose|p)|d(oc(byanchor(obj)?|ument_(s(etcontent|ize)|attributes|bodytag|content))|eleteobject|ummy)|e(rror(msg)?|dittext)|get(an(chors(obj)?|dlock)|child(coll(obj)?|doccoll(obj)?)|object(byquery(coll(obj)?|obj)?)?|parents(obj)?|re(mote(children)?|llink)|srcbydestobj|text|username)|i(n(s(ert(anchors|(documen|objec)t)|coll|doc)|collections|fo)|dentify)|m(apid|odifyobject|v)|o(bjrec2array|utput_document)|p(connec|ipedocumen)t|s(etlinkroo|ta)t|array2objrec|((free|new)_documen|roo)t|unlock|who)|api_(attribute(_(values?|key|langdepvalue))?|c(h(eck(in|out)|ildren)|o(ntent(_(mimetype|read))?|py))|d(st(ofsrc)?anchors|[bc]stat)|error_(count|reason)|f(ind|tstat)|h(gcsp|wstat)|i(n(sert(anchor|collection|document)?|fo)|dentify)|l(in|oc)k|object(_(a(ssign|ttreditable)|(coun|inser)t|new|(remov|titl|valu)e)|byanchor)?|re(ason_(description|type)|(mov|plac)e)|s(rc(anchors|sofdst)|etcommitedversion)|u(ser(list)?|nlock)|move|new_content|parents))|ypot)|i(base_(a(dd_user|ffected_rows)|b(lob_(c(ancel|(los|reat)e)|i(mport|nfo)|add|echo|get|open)|ackup)|c(o(mmit(_ret)?|nnect)|lose)|d(b_info|elete_user|rop_db)|e(rr(code|msg)|xecute)|f(etch_(assoc|object|row)|ree_(event_handler|query|result)|ield_info)|m(aintain_db|odify_user)|n(um_(field|param)s|ame_result)|p(aram_info|connect|repare)|r(ollback(_ret)?|estore)|se(rv(ice_(at|de)tach|er_info)|t_event_handler)|t(imefmt|rans)|gen_id|query|wait_event)|conv(_(mime_(decode(_headers)?|encode)|s(tr(len|r?pos)|et_encoding|ubstr)|get_encoding))?|d(3_(get_(genre_(id|list|name)|tag|version)|(remove|set)_tag)|ate)|fx(_(b(lobinfile_mode|yteasvarchar)|c(o(nnect|py_blob)|reate_(blob|char)|lose)|error(msg)?|f(ield(properti|typ)es|ree_(blob|char|result)|etch_row)|get(_(blob|char)|sqlca)|nu(m_(field|row)s|llformat)|p(connect|repare)|update_(blob|char)|affected_rows|do|htmltbl_result|query|textasvarchar)|us_(c(los|reat)e_slob|((fre|writ)e|open|read|seek|tell)_slob))|m(a(ge(_type_to_(extension|mime_type)|a(lphablending|ntialias|rc)|c(har(up)?|o(lor(a(llocate(alpha)?|t)|closest(alpha|hwb)?|exact(alpha)?|resolve(alpha)?|s(et|forindex|total)|deallocate|match|transparent)|py(merge(gray)?|res(ampl|iz)ed)?)|reate(from(g(d(2(part)?)?|if)|x[bp]m|(jpe|(p|stri)n)g|wbmp)|truecolor)?)|d(ashedline|estroy)|f(il(l(ed(arc|(ellips|rectangl)e|polygon)|toborder)?|ter)|ont(height|width)|t(bbox|text))|g(d2?|ammacorrect|if)|i(nterlace|struecolor)|l((ayereffec|oadfon)t|ine)|p(s(e(ncode|xtend)font|bbox|((copy|free|load|slant)fon|tex)t)|alettecopy|ng|olygon)|r(ectangl|otat)e|s(et(t(hickness|ile)|brush|pixel|style)|tring(up)?|avealpha|[xy])|t(tf(bbox|text)|ruecolortopalette|ypes)|2?wbmp|ellipse|jpeg|xbm)|p_(a(lerts|ppend)|b(ody(struct)?|ase64|inary)|c(l(earflag_full|ose)|heck|reatemailbox)|delete(mailbox)?|e(rrors|xpunge)|fetch(_overview|body|header|structure)|get(_quota(root)?|acl|mailboxes|subscribed)|header(info|s)?|l(ist(s(can|ubscribed)|mailbox)?|ast_error|sub)|m(ail(_(co(mpose|py)|move)|boxmsginfo)?|ime_header_decode|sgno)|num_(msg|recent)|r(e(namemailbox|open)|fc822_(parse_(adrlist|headers)|write_address))|s(e(t(_quota|(ac|flag_ful)l)|arch)|canmailbox|ort|tatus|ubscribe)|t(hread|imeout)|u(n(delet|subscrib)e|tf(7_(de|en)code|8)|id)|(8bi|qprin)t|open|ping))|p(lode|ort_request_variables))|n(clude(_once)?|et_(ntop|pton)|gres_(c(o(mmi|nnec)t|lose)|f(etch_(array|object|row)|ield_(n(am|ullabl)e|length|precision|(scal|typ)e))|num_(field|row)s|(autocommi|pconnec)t|query|rollback)|i_(get(_all)?|alter|restore|set)|_array|tval)|p(tc(embed|parse)|2long)|rcg_(i(gnore_(add|del)|(nvit|s_conn_aliv)e)|l(ist|(ookup_format_message|user)s)|n(ick(name_(un)?escape)?|ames|otice)|p(ar|connec)t|set_(current|(fil|on_di)e)|who(is)?|((channel_m|html_enc)od|get_usernam)e|disconnect|(eval_ecmascript_param|register_format_message)s|(fetch_error_)?msg|join|kick|oper|topic)|s(_(a(rray)?|d(ir|ouble)|f(i(l|nit)e|loat)|in(t(eger)?|finite)|l(ink|ong)|n(u(ll|meric)|an)|re(a(dable|l)|source)|s(calar|oap_fault|tring|ubclass_of)|write?able|bool|((call|execut)ab|uploaded_fi)le|object)|set)|gnore_user_abort)|j(ava_last_exception_(clear|get)|d(to(j(ewish|ulian)|french|gregorian|unix)|dayofweek|monthname)|(ewish|ulian)tojd|oin|peg2wbmp)|k(ey|r?sort)|l(dap_(c(o(mpare|nnect|unt_entries)|lose)|d(elete|n2ufn)|e(rr((2st|o)r|no)|xplode_dn)|f(irst_((attribut|referenc)e|entry)|ree_result)|get_(values(_len)?|(attribut|entri)es|(d|optio)n)|mod(_(add|del|replace)|ify)|next_((attribut|referenc)e|entry)|parse_re(ference|sult)|re(ad|name)|s(e(t_(option|rebind_proc)|arch)|asl_bind|ort|tart_tls)|8859_to_t61|(ad|(un)?bin)d|list|t61_to_8859)|i(mititerator_(getposition|next|(rewin|vali)d|seek)|nk(info)?|st)|o(cal(econv|time)|g(1[0p])?|ng2ip)|zf_((de)?compress|optimized_for)|cg_value|evenshtein|stat|trim)|m(a(i(l(parse_(msg_(extract_part(_file)?|get_(part(_data)?|structure)|parse(_file)?|(creat|fre)e)|determine_best_xfer_encoding|rfc822_parse_addresses|stream_encode|uudecode_all))?|n)|x)|b_(convert_(case|encoding|kana|variables)|de(code_(mimeheader|numericentity)|tect_(encoding|order))|e(ncode_(mimeheader|numericentity)|reg(_(search(_(get(po|reg)s|init|((set)?po|reg)s))?|match|replace)|i(_replace)?)?)|http_(in|out)put|l(anguage|ist_encodings)|p(arse_str|referred_mime_name)|regex_(encoding|set_options)|s(tr(to(low|upp)er|cut|(im)?width|len|r?pos)|ubst(r(_count)?|itute_character)|end_mail|plit)|get_info|internal_encoding|output_handler)|c(al_(c(lose|reate_calendar)|d(a(te_(compare|valid)|y(_of_(week|year)|s_in_month))|elete_(calendar|event))|e(vent_(set_(c(ategory|lass)|recur_(monthly_[mw]day|(dai|week|year)ly|none)|alarm|description|end|start|title)|add_attribute|init)|xpunge)|fetch_(current_stream_)?event|list_(alarm|event)s|re(name_calendar|open)|s(nooze|tore_event)|append_event|(is_leap|week_of)_year|next_recurrence|p?open|time_valid)|rypt_(c(bc|fb|reate_iv)|e(nc(_(get_(((algorithm|mode)s_nam|(block|iv|key)_siz)e|supported_key_sizes)|is_block_(algorithm(_mode)?|mode)|self_test)|rypt)|cb)|ge(neric(_((de)?init|end))?|t_((block|iv|key)_siz|cipher_nam)e)|list_(algorithm|mode)s|module_(get_(algo_(block|key)_size|supported_key_sizes)|is_block_(algorithm(_mode)?|mode)|close|open|self_test)|decrypt|ofb)|ve_(adduser(arg)?|c(h(eckstatus|(k|ng)pwd)|o(nnect(ionerror)?|mpleteauthorizations))|d(e(l(ete(response|trans|usersetup)|user)|stroy(conn|engine))|isableuser)|e(dit|nable)user|g(et(c(ell(bynum)?|ommadelimited)|user(arg|param)|header)|[fu]t|l)|i(nit(conn|engine|usersetup)|scommadelimited)|list(stat|user)s|m(axconntimeout|onitor)|num(column|row)s|p(reauth(completion)?|arsecommadelimited|ing)|re(turn(code|status)?|sponseparam)|s(et(ssl(_files)?|t(imeout|le)|blocking|dropfile|ip)|ale)|t(ext_(c(ode|v)|avs)|rans(action(a(uth|vs)|i(d|tem)|batch|cv|(ssen|tex)t)|inqueue|new|param|send))|u(b|wait)|v(erify(connection|sslcert)|oid)|bt|(forc|overrid)e|qc))|d(5(_file)?|ecrypt_generic)|e(m(cache_(c(lose|onnect)|de(bug|crement|lete)|get(stats|version)?|add|flush|(incremen|pconnec|se)t|replace)|ory_get_usage)|t(aphone|hod_exists))|hash(_(get_(block_siz|hash_nam)e|count|keygen_s2k))?|i(n(g_(set(cubicthreshold|scale)|useswfversion))?|(crotim|me_content_typ)e)|k(dir|time)|o(ney_format|ve_uploaded_file)|s(ession_(c(o(nnec|un)t|reate)|d(estroy|isconnect)|get(_(array|data))?|l(ist(var)?|ock)|set(_(array|data))?|un(iq|lock)|find|inc|plugin|randstr|timeout)|g_(re(ceiv|move_queu)e|s(e(nd|t_queue)|tat_queue)|get_queue)|ql(_(c(reate_?db|lose|onnect)|d(b(_query|name)|ata_seek|rop_db)|f(etch_(array|field|object|row)|ield(_(t(abl|yp)e|flags|len|name|seek)|t(abl|yp)e|flags|len|name)|ree_result)|list_(db|field|table)s|num(_(field|row)s|(field|row)s)|re(gcase|sult)|affected_rows|error|pconnect|query|select_db|tablename))?|sql_(c(lose|onnect)|f(etch_(a(rray|ssoc)|batch|field|object|row)|ield_(length|(nam|typ)e|seek)|ree_(resul|statemen)t)|g(et_last_message|uid_string)|min_(error|message)_severity|n(um_(field|row)s|ext_result)|r(esult|ows_affected)|bind|data_seek|execute|(ini|pconnec)t|query|select_db))|t_(getrandmax|s?rand)|uscat_(g(et|ive)|setup(_net)?|close)|ysql(_(c(l(ient_encoding|ose)|hange_user|onnect|reate_db)|d(b_(name|query)|ata_seek|rop_db)|e(rr(no|or)|scape_string)|f(etch_(a(rray|ssoc)|field|lengths|object|row)|ield_(t(abl|yp)e|flags|len|name|seek)|ree_result)|get_((clien|hos)t|proto|server)_info|in(fo|sert_id)|list_(db|field|(process|tabl)e)s|num_(field|row)s|p(connect|ing)|re(al_escape_string|sult)|s(elect_db|tat)|t(ablename|hread_id)|affected_rows|(unbuffered_)?query)|i_(a(ffected_rows|utocommit)|bind_(param|result)|c(ha(nge_user|racter_set_name)|l(ient_encoding|ose)|o(nnect(_err(no|or))?|mmit))|d(isable_r(eads_from_master|pl_parse)|ata_seek|ebug|ump_debug_info)|e(nable_r(eads_from_master|pl_parse)|rr(no|or)|mbedded_connect|scape_string|xecute)|f(etch(_(a(rray|ssoc)|field(_direct|s)?|lengths|object|row))?|ield_(count|seek|tell)|ree_result)|get_(client_(info|version)|server_(info|version)|(host|proto)_info|metadata)|in(fo|it|sert_id)|m((aster|ulti)_query|ore_results)|n(um_(field|row)s|ext_result)|p(aram_count|ing|repare)|r(e(al_(connect|escape_string|query)|port)|pl_(p(arse_enabled|robe)|query_type)|ollback)|s(e(nd_(long_data|query)|rver_(end|init)|lect_db|t_opt)|t(mt_(bind_(param|result)|e(rr(no|or)|xecute)|f(etch|ree_result)|p(aram_count|repare)|res(et|ult_metadata)|s(end_long_data|qlstate|tore_result)|(affected|num)_rows|close|data_seek|init)|(a|ore_resul)t)|qlstate|sl_set)|thread_(id|safe)|kill|options|query|(use_resul|warning_coun)t)))|n(at(case)?sort|curses_(a(dd(ch(n?str)?|n?str)|ttr(o(ff|n)|set)|ssume_default_colors)|b(kgd(set)?|o(rder|ttom_panel)|audrate|eep)|c(l(rto(bot|eol)|ear)|olor_(conten|se)t|an_change_color|break|urs_set)|d(e(f(_(prog|shell)_mode|ine_key)|l(_panel|ay_output|ch|(etel|wi)n))|oupdate)|e(cho(char)?|rase(char)?|nd)|f(l(ash|ushinp)|ilter)|get(m(axyx|ouse)|ch|yx)|h(a(s_(i[cl]|colors|key)|lfdelay)|ide_panel|line)|i(n(it(_(colo|pai)r)?|s(ch|(del|ert)ln|s?tr)|ch)|sendwin)|k(ey(ok|pad)|illchar)|m(o(use(_trafo|interval|mask)|ve(_panel)?)|v(add(ch(n?str)?|n?str)|(cu|waddst)r|(del|get|in)ch|[hv]line)|eta)|n(ew(_panel|pad|win)|o(cbreak|echo|nl|qiflush|raw)|apms|l)|p(a(nel_(above|(bel|wind)ow)|ir_content)|(nout)?refresh|utp)|r(e(set(_(prog|shell)_mode|ty)|fresh|place_panel)|aw)|s(cr(_(dump|(ini|se)t|restore)|l)|lk_(attr(o(ff|n)|set)?|c(lea|olo)r|re(fresh|store)|(ini|se)t|(noutrefres|touc)h)|ta(nd(end|out)|rt_color)|avetty|how_panel)|t(erm(attrs|name)|imeout|op_panel|ypeahead)|u(nget(ch|mouse)|se_(e(nv|xtended_names)|default_colors)|pdate_panels)|v(idattr|line)|w(a(dd(ch|str)|ttr(o(ff|n)|set))|c(lear|olor_set)|mo(use_trafo|ve)|stand(end|out)|border|(eras|[hv]lin)e|(getc|(nout)?refres)h)|longname|qiflush)|l(2br|_langinfo)|otes_(c(reate_(db|note)|opy_db)|mark_(un)?read|body|drop_db|(find_no|nav_crea)te|header_info|list_msgs|search|unread|version)|sapi_(re(quest|sponse)_headers|virtual)|((gett)?ex|umber_forma)t)|o(b_(end_(clean|flush)|g(et_(c(lean|ontents)|le(ngth|vel)|flush|status)|zhandler)|i(conv_handler|mplicit_flush)|clean|flush|list_handlers|start|tidyhandler)|c(i(_(c(o(llection_(a(ppend|ssign)|element_(assign|get)|max|size|trim)|(mmi|nnec)t)|ancel|lose)|e(rror|xecute)|f(etch(_(a(ll|rray|ssoc)|object|row))?|ield_(s(cal|iz)e|type(_raw)?|is_null|name|precision)|ree_(collection|descriptor|statement))|lob_(c(lose|opy)|e(of|rase|xport)|i(mport|s_equal)|re(a|win)d|s((av|iz)e|eek)|t(ell|runcate)|write(_temporary)?|(appen|loa)d|flush)|n(ew_(c(o(llection|nnect)|ursor)|descriptor)|um_(field|row)s)|p(a(rs|ssword_chang)e|connect)|r(esult|ollback)|s(e(rver_version|t_prefetch)|tatement_type)|(bind|define)_by_name|internal_debug)|c(o(l(l(a(ssign(elem)?|ppend)|(getele|tri)m|max|size)|umn(s(cal|iz)e|type(raw)?|isnull|name|precision))|mmit)|ancel|loselob)|e(rror|xecute)|f(etch(into|statement)?|ree(c(ollection|ursor)|desc|statement))|lo(go(ff|n)|adlob)|n(ew(c(ollection|ursor)|descriptor)|logon|umcols)|p(arse|logon)|r(o(llback|wcount)|esult)|s(avelob(file)?|e(t(bufferinglob|prefetch)|rverversion)|tatementtype)|write(lobtofile|temporarylob)|(bind|define)byname|getbufferinglob|internaldebug)|tdec)|dbc_(c(lose(_all)?|o(lumn(privilege)?s|(mmi|nnec)t)|ursor)|d(ata_source|o)|e(rror(msg)?|xec(ute)?)|f(etch_(array|into|object|row)|ield_(n(ame|um)|(le|precisio)n|(scal|typ)e)|oreignkeys|ree_result)|n(um_(field|row)s|ext_result)|p(r(ocedure(column)?s|epare|imarykeys)|connect)|r(esult(_all)?|ollback)|s(etoption|(pecialcolumn|tatistic)s)|table(privilege)?s|autocommit|binmode|gettypeinfo|longreadlen)|pen(ssl_(csr_(export(_to_file)?|new|sign)|get_p(rivate|ublic)key|p(k(cs7_((de|en)crypt|sign|verify)|ey_(export(_to_file)?|get_p(rivate|ublic)|new))|rivate_(de|en)crypt|ublic_(de|en)crypt)|s(eal|ign)|x509_(check(_private_key|purpose)|export(_to_file)?|(fre|pars)e|read)|error_string|(free_ke|verif)y|open)|dir|log)|r(a_(c(o(lumn(nam|siz|typ)e|mmit(o(ff|n))?)|lose)|e(rror(code)?|xec)|fetch(_into)?|logo(ff|n)|num(col|row)s|p(arse|logon)|bind|do|(getcolum|ope)n|rollback)|d)|utput_(add_rewrite_var|reset_rewrite_vars)|v(rimos_(c(o(mmi|nnec)t|lose|ursor)|exec(ute)?|f(etch_(into|row)|ield_(n(ame|um)|len|type)|ree_result)|num_(field|row)s|r(esult(_all)?|ollback)|longreadlen|prepare)|erload))|p(a(r(entiterator_((get|has)children|next|rewind)|se(_(ini_file|str|url)|kit_(compile_(file|string)|func_arginfo)))|ck|ssthru|thinfo)|c(ntl_(s(etpriority|ignal)|w(ait(pid)?|if(s(ignal|topp)ed|exited)|exitstatus|(stop|term)sig)|alarm|exec|fork|getpriority)|lose)|df_(a(dd_(l(aunch|ocal)link|annotation|(bookmar|(pdf|web)lin)k|(not|outlin)e|thumbnail)|rcn?|ttach_file)|begin_(pa(ge|ttern)|template)|c(l(ose(_(pdi(_page)?|image)|path(_(fill_)?stroke)?)?|ip)|on(ca|tinue_tex)t|ircle|urveto)|end(_(pa(ge|ttern)|template)|path)|fi(ll(_stroke)?|ndfont)|get_(font((nam|siz)e)?|image_(height|width)|m(aj|in)orversion|p(di_(parameter|value)|arameter)|buffer|value)|m(akespotcolor|oveto)|open(_(image(_file)?|p(di(_page)?|ng)|ccitt|(fil|memory_imag)e|(gi|tif)f|jpeg))?|place_(im|pdi_p)age|r(e(ct|store)|otate)|s(et(_(border_(color|dash|style)|info(_((auth|creat)or|keywords|subject|title))?|text_(r(endering|ise)|matrix|pos)|((char|word)_spac|horiz_scal|lead)ing|duration|font|parameter|value)|f(la|on)t|gray(_(fill|stroke))?|line(cap|join|width)|m(atrix|iterlimit)|rgbcolor(_(fill|stroke))?|color|(poly)?dash)|how(_(boxed|xy))?|tr(ingwidth|oke)|(av|cal)e|kew)|(dele|transla)te|initgraphics|lineto|new)|f(pro_(process(_raw)?|cleanup|init|version)|sockopen)|g_(c(l(ient_encoding|ose)|o(n(nect(ion_(busy|reset|status))?|vert)|py_(from|to))|ancel_query)|d(bnam|elet)e|e(scape_(bytea|string)|nd_copy)|f(etch_(a(ll|rray|ssoc)|r(esult|ow)|object)|ield_(n(ame|um)|is_null|prtlen|(siz|typ)e)|ree_result)|get_(notify|pid|result)|l(ast_(error|notice|oid)|o_(c(los|reat)e|read(_all)?|(ex|im)port|open|(see|unlin)k|tell|write))|num_(field|row)s|p(arameter_status|(connec|or)t|ing|ut_line)|result_(s(eek|tatus)|error)|se(lect|nd_query|t_client_encoding)|t(race|ty)|u(n(escape_bytea|trace)|pdate)|(affected_row|option)s|(hos|inser)t|meta_data|query|version)|hp(_(s(api_nam|trip_whitespac)e|check_syntax|ini_scanned_files|logo_guid|uname)|credits|info|version)|o(s(ix_(get(e[gu]id|g(r(gid|nam|oups)|id)|p(g(id|rp)|w(nam|uid)|p?id)|_last_error|(cw|[su]i)d|login|rlimit)|s(et(e[gu]id|(p?g|[su])id)|trerror)|t(imes|tyname)|ctermid|isatty|kill|mkfifo|uname))?|pen|w)|r(e(g_(match(_all)?|replace(_callback)?|grep|quote|split)|v)|int(er_(c(reate_(brush|dc|font|pen)|lose)|d(elete_(brush|dc|font|pen)|raw_(r(ectangle|oundrect)|bmp|chord|(elips|lin|pi)e|text))|end_(doc|page)|l(is|ogical_fontheigh)t|s(e(lect_(brush|font|pen)|t_option)|tart_(doc|page))|abort|(get_optio|ope)n|write)|_r|f)?|oc_((clos|nic|terminat)e|get_status|open))|spell_(add_to_(personal|session)|c(onfig_(d(ata|ict)_dir|r(epl|untogether)|(creat|ignor|mod)e|(persona|save_rep)l)|heck|lear_session)|new(_(config|personal))?|s((ave_wordli|ugge)s|tore_replacemen)t)|i|ng2wbmp|utenv)|q(dom_(error|tree)|uote(d_printable_decode|meta))|r(a(n(d|ge)|wurl(de|en)code|d2deg)|e(a(d(lin(e(_(c(allback_(handler_(install|remove)|read_char)|lear_history|ompletion_function)|((ad|rea)d|list|write)_history|info))?|k)|_exif_data|dir|(gz)?file)|lpath)|c(ode(_(file|string))?|ursive(directoryiterator_((get|has)children|key|next|rewind)|iteratoriterator_(get(depth|subiterator)|(curren|nex)t|key|(rewin|vali)d)))|gister_(shutdown|tick)_function|quire(_once)?|s(tore_(e(rror|xception)_handler|include_path)|et)|wind(dir)?|name|turn)|mdir|ound|sort|trim)|s(e(m_(re(leas|mov)e|acquire|get)|s(am_(co(mmi|nnec)t|di(agnostic|sconnect)|e(rrormsg|xecimm)|f(etch_(r(esult|ow)|array)|ield_(array|name)|ree_result)|se(ek_row|ttransaction)|(affected_row|num_field)s|query|rollback)|sion_(c(ache_(expire|limiter)|ommit)|de(code|stroy)|i(s_registere)?d|reg(enerate_id|ister)|s(et_(cookie_params|save_handler)|ave_path|tart)|un(register|set)|(encod|(module_)?nam|write_clos)e|get_cookie_params))|t(_(e(rror|xception)_handler|file_buffer|include_path|magic_quotes_runtime|time_limit)|((raw)?cooki|local|typ)e)|rialize)|h(a1(_file)?|m(_(remove(_var)?|(at|de)tach|(ge|pu)t_var)|op_((clos|(dele|wri)t|siz)e|open|read))|ell_exec|(ow_sourc|uffl)e)|i(m(plexml(_(element_(a(sxml|ttributes)|children|xpath)|load_(file|string)|import_dom)|iterator_((curren|nex)t|(get|has)children|key|(rewin|vali)d))|ilar_text)|nh?|zeof)|nmp(_(get_(quick_print|valueretrieval)|set_((enum|oid_numeric|quick)_print|valueretrieval)|read_mib)|get(next)?|walk(oid)?|realwalk|set)|o(ap(client_(get(lastre(quest|sponse)|(function|type)s)|call|soapclient)|server_(s(et(class|persistence)|oapserver)|addfunction|getfunctions|handle)|fault_soapfault|(header_soapheade|var_soapva)r|param_soapparam)|cket_(c(l(ear_error|ose)|reate(_(listen|pair))?|onnect)|get(_(option|status)|(peer|sock)name)|l(ast_error|isten)|re(cv(from)?|ad)|s(e(nd(to)?|t_(block(ing)?|nonblock|option|timeout)|lect)|hutdown|trerror)|accept|bind|write)|rt|undex)|p(liti?|rintf)|q(l(ite_(c(reate_(aggregate|function)|hanges|lose|olumn|urrent)|e((rror|scape)_string|xec)|f(etch_(a(ll|rray)|s(ingle|tring)|column_types|object)|actory|ield_name)|has_(more|prev)|l(ast_(error|insert_rowid)|ib(encoding|version))|n(um_(field|row)s|ext)|p(open|rev)|s(eek|ingle_query)|u(df_(de|en)code_binary|nbuffered_query)|(array_)?query|busy_timeout|open|rewind)|_regcase)|rt)|t(r(_(r(ep(eat|lace)|ot13)|s(huffle|plit)|ireplace|pad|word_count)|c((asec)?mp|hr|oll|spn)|eam_(co(ntext_(get_(default|options)|set_(option|params)|create)|py_to_stream)|filter_((ap|pre)pend|register)|get_(((conten|transpor)t|(filt|wrapp)er)s|line|meta_data)|s(e(t_(blocking|timeout|write_buffer)|lect)|ocket_(se(ndto|rver)|(accep|clien)t|enable_crypto|get_name|recvfrom))|(register_wrapp|wrapper_regist)er)|i(p(_tag|c?slashe|o)s|str)|n(atc(asec)?mp|c(asec)?mp)|p(brk|os)|r(chr|ev|i?pos)|s(pn|tr)|t(o(k|(low|upp)er|time)|r)|ftime|len|val)|at)|ubstr(_(co(mpare|unt)|replace))?|wf(_(a(ction(g(oto(frame|label)|eturl)|p(lay|revframe)|s(ettarget|top)|(next|waitfor)frame|togglequality)|dd(buttonrecord|color))|define(bitmap|(fon|rec|tex)t|line|poly)|end(s(hape|ymbol)|(butt|doacti)on)|font(s(ize|lant)|tracking)|get(f(ontinfo|rame)|bitmapinfo)|l(abelframe|ookat)|m(odifyobject|ulcolor)|o(rtho2?|ncondition|penfile)|p(o(larview|pmatrix|sround)|erspective|laceobject|ushmatrix)|r(emoveobject|otate)|s(etf(ont|rame)|h(ape(curveto3?|fill(bitmap(clip|tile)|off|solid)|line(solid|to)|arc|moveto)|owframe)|tart(s(hape|ymbol)|(butt|doacti)on)|cale)|t(extwidth|ranslate)|closefile|nextid|viewport)|b(itmap(.get(height|width))?|utton(.(add(action|shape)|set((actio|dow)n|hit|over|up))|_keypress)?)|displayitem(.(m(ove(to)?|ultcolor)|r(otate(to)?|emove)|s(cale(to)?|et(depth|name|ratio)|kew(x(to)?|y(to)?))|addcolor))?|f(ill(.(s(kew[xy]to|caleto)|(mov|rotat)eto))?|ont(.getwidth)?)|gradient(.addentry)?|mo(rph(.getshape[12])?|vie(.(s(et(background|dimension|frames|rate)|ave|treammp3)|add|(nextfram|remov)e|output))?)|s(hape(.(draw(curve(to)?|line(to)?)|movepen(to)?|set(l(eftfill|ine)|rightfill)|addfill))?|prite(.(add|(nextfram|remov)e|setframes))?)|text(.(set(color|(fon|heigh)t|spacing)|addstring|getwidth|moveto)|field(.(a(ddstring|lign)|set(l(eftmargin|inespacing)|(bound|margin)s|color|(fon|heigh)t|(indentatio|rightmargi)n|name)))?)?|action)|y(base_(c(lose|onnect)|d(ata_seek|eadlock_retry_count)|f(etch_(a(rray|ssoc)|field|object|row)|ield_seek|ree_result)|min_(client|(erro|serve)r|message)_severity|num_(field|row)s|se(lect_db|t_message_handler)|affected_rows|get_last_message|(pconnec|resul)t|(unbuffered_)?query)|s(log|tem)|mlink)|candir|leep|rand|scanf)|t(anh?|e(mpnam|xtdomain)|i(dy_(c(on(fig_coun|struc)t|lean_repair)|get(_(h(tml(_ver)?|ead)|r(elease|oot)|body|config|error_buffer|output|status)|opt)|is_x(ht)?ml|node_(get_(attr|nodes)|has(children|siblings)|is(x(ht)?ml|(as|ph)p|(commen|tex)t|html|jste)|attributes|children|next|prev|tidy_node)|parse_(file|string)|re(pair_(file|string)|set_config)|s(et(_encoding|opt)|ave_config)|(access|error|warning)_count|diagnose|load_config)|me(_nanosleep)?)|o(ken_(get_all|name)|uch)|ri(gger_error|m)|cpwrap_check|mpfile)|u(c(first|words)|dm_(a(lloc_agent(_array)?|dd_search_limit|pi_version)|c(at_(list|path)|heck_(charset|stored)|l(ear_search_limits|ose_stored)|rc32)|err(no|or)|f(ree_(agent|ispell_data|res)|ind)|get_(res_(field|param)|doc_count)|hash32|load_ispell_data|open_stored|set_agent_param)|n(i(qi|xtoj)d|se(rialize|t)|(lin|pac)k|register_tick_function)|rl(de|en)code|s(er_error|leep|ort)|tf8_(de|en)code|[ak]sort|mask)|v(ar(_(dump|export)|iant(_(a(bs|[dn]d)|c(as?t|mp)|d(ate_(from|to)_timestamp|iv)|i(div|mp|nt)|m(od|ul)|n(eg|ot)|s(et(_type)?|ub)|eqv|fix|get_type|x?or|pow|round))?)|p(opmail_(a(dd_(alias_domain(_ex)?|domain(_ex)?|user)|lias_(del(_domain)?|get(_all)?|add)|uth_user)|del_(domain(_ex)?|user)|error|passwd|set_user_quota)|rintf)|ersion_compare|[fs]printf|irtual)|w(32api_(in(it_dtype|voke_function)|deftype|register_function|set_call_method)|ddx_(packet_(end|start)|serialize_va(lue|rs)|add_vars|deserialize)|ordwrap)|x(attr_(s(et|upported)|(ge|lis)t|remove)|diff_(file_(diff(_binary)?|patch(_binary)?|merge3)|string_(diff(_binary)?|patch(_binary)?|merge3))|ml(_(get_(current_(byte_index|(column|line)_number)|error_code)|parse(r_(create(_ns)?|free|[gs]et_option)|_into_struct)?|set_(e(lement|nd_namespace_decl|xternal_entity_ref)_handler|(character_data|default|(notation|start_namespace|unparsed_entity)_decl|processing_instruction)_handler|object)|error_string)|rpc_(decode(_request)?|encode(_request)?|se(rver_(c(all_method|reate)|register_(introspection_callback|method)|add_introspection_data|destroy)|t_type)|get_type|is_fault|parse_method_descriptions))|p(ath_(eval(_expression)?|new_context)|tr_(eval|new_context))|sl(_xsltprocessor_(re(gister_php_functions|move_parameter)|transform_to_(doc|uri|xml)|[gs]et_parameter|(has_exslt_suppor|import_styleshee)t)|t_(backend_(info|name|version)|err(no|or)|set(_(e(ncoding|rror_handler)|s(ax_handlers?|cheme_handlers?)|base|log|object)|opt)|(creat|fre)e|getopt|process)))|y(az_(c(cl_(conf|parse)|lose|onnect)|e(rr(no|or)|(lemen|s_resul)t)|r(ange|ecord)|s(c(an(_result)?|hema)|e(arch|t_option)|ort|yntax)|addinfo|database|get_option|hits|itemorder|(presen|wai)t)|p_(err(_string|no)|ma(ster|tch)|all|(ca|firs|nex)t|get_default_domain|order))|z(end_(logo_guid|version)|ip_(entry_(c(ompress(edsize|ionmethod)|lose)|(filesiz|nam)e|open|read)|close|open|read)|lib_get_coding_type))\b/ {

    function_name_face (true);
    language_print ($0);
    function_name_face (false);
  }
  
  /\b(include|if|elseif|include_once|require|require_once|while|for|function|
  return|case|default|global|switch|else|break|return|as|foreach|var|const|class|__construct|__deconstruct)\b/ {

    keyword_face (true);
    language_print ($0);
    keyword_face (false);
  }

  LANGUAGE_SPECIALS {
    language_print ($0);
  }
}

