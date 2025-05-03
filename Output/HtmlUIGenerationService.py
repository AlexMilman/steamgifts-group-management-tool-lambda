# HTML response generation service of SGMT
# Copyright (C) 2017  Alex Milman


def generate_main_page_ui():
    response = get_header('SteamGifts Group Management Tool (SGMT)')
    response += '<main>'
    response += '<section class="section"><h4>Group Management</h4>'
    response += '<div class="grid">'
    response += '<a class="card" href="/SGMT/UserCheckRulesUI">UserCheckRules<br><small>Check user compliance</small></a>'
    response += '<a class="card" href="/SGMT/CheckMonthlyUI">CheckMonthly<br><small>Users without giveaways</small></a>'
    response += '<a class="card" href="/SGMT/CheckAllGiveawaysAccordingToRulesUI">CheckAllGiveawaysAccordingToRules<br><small>Validate giveaway rules</small></a>'
    response += '<a class="card" href="/SGMT/UserCheckFirstGiveawayUI">UserCheckFirstGiveaway<br><small>First giveaway rules</small></a>'
    response += '<a class="card" href="/SGMT/GroupUsersSummaryUI">GroupUsersSummary<br><small>Group summary</small></a>'
    response += '<a class="card" href="/SGMT/UserFullGiveawaysHistoryUI">UserFullGiveawaysHistory<br><small>Detailed history</small></a>'
    response += '<a class="card" href="/SGMT/PopularGiveawaysUI">PopularGiveaways<br><small>Top giveaways</small></a>'
    response += '<a class="card" href="/SGMT/CheckGameGiveawaysUI">CheckGameGiveaways<br><small>Entries per game</small></a>'
    response += '</div></section>'
    response += '<section class="section"><h4>Tool Management</h4>'
    response += '<div class="grid">'
    response += '<a class="card" href="/SGMT/GetAvailableGroups">GetAvailableGroups<br><small>List groups</small></a>'
    response += '<a class="card" href="/SGMT/AddNewGroupUI">AddNewGroup<br><small>Add new group</small></a>'
    response += '</div></section>'
    response += '</main>'
    response += get_footer()
    return response

def get_header(title, action=None, head=None):
    response = '<!DOCTYPE html><html lang="en">'
    response += '<head>'
    response += '<meta charset="UTF-8">'
    response += '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    response += '<style>'
    response += '''
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
        margin: 0; padding: 0; background: #f8fafc; color: #1e293b;
    }
    header {
        background: #1e3a8a;
        padding: 20px;
        color: #fff;
    }
    header h1 {
        margin: 0;
        font-size: 1.8em;
    }
    nav {
        margin-top: 10px;
    }
    nav a {
        color: #cbd5e1;
        margin-right: 20px;
        text-decoration: none;
        font-size: 0.95em;
    }
    nav a:hover {
        color: #fff;
    }
    .container {
        max-width: 960px;
        margin: 0 auto;
        padding: 30px 20px;
    }
    .section {
        margin-bottom: 40px;
    }
    .section h4 {
        font-size: 1.3em;
        margin-bottom: 15px;
        color: #0f172a;
    }
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 20px;
    }
    .card {
        background: #fff;
        border-radius: 10px;
        padding: 20px;
        text-align: left;
        text-decoration: none;
        color: #1e293b;
        box-shadow: 0 4px 6px rgba(0,0,0,0.06);
        transition: box-shadow 0.2s ease-in-out;
    }
    .card:hover {
        box-shadow: 0 8px 12px rgba(0,0,0,0.1);
    }
    .card small {
        display: block;
        color: #64748b;
        margin-top: 8px;
    }
    footer {
        padding: 20px;
        text-align: center;
        color: #94a3b8;
    }
    input[type="date"] {
        padding: 8px;
        font-size: 1em;
        border: 1px solid #ccc;
        border-radius: 6px;
        background-color: #fff;
    }
.button, input[type="submit"] {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    padding: 10px 20px;
    font-size: 0.95em;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}
.button:hover, input[type="submit"]:hover {
    background-color: #1e40af;
}

    '''
    response += '</style>'
    if head:
        response += head
    response += '</head><body>'
    response += f'<header><div class="container"><h1>{title}</h1>'
    response += '<nav>'
    response += '<a href="/SGMT">Home</a>'
    response += '<a href="/SGMT/UserCheckRulesUI">UserCheckRules</a>'
    response += '<a href="/SGMT/CheckMonthlyUI">CheckMonthly</a>'
    response += '<a href="/SGMT/CheckAllGiveawaysAccordingToRulesUI">CheckAllGiveawaysAccordingToRules</a>'
    response += '<a href="/SGMT/UserCheckFirstGiveawayUI">UserCheckFirstGiveaway</a>'
    response += '<a href="/SGMT/GroupUsersSummaryUI">GroupUsersSummary</a>'
    response += '<a href="/SGMT/UserFullGiveawaysHistoryUI">UserFullGiveawaysHistory</a>'
    response += '<a href="/SGMT/PopularGiveawaysUI">PopularGiveaways</a>'
    response += '<a href="/SGMT/CheckGameGiveawaysUI">CheckGameGiveaways</a>'
    response += '</nav></div></header>'
    response += '<div class="container">'
    if action:
        response += f'<form action="/SGMT/{action}">'
    return response



def get_footer(button_text=None):
    response = '<BR>'
    if button_text:
        response += '<div class="form-actions"><input type="submit" class="button" value="' + button_text + '"/></div></form>'
    response += '<footer><small><a href="/SGMT/legal">Legal</a> | Support: <a href="mailto:sgmt.suport@gmail.com">sgmt.suport@gmail.com</a></small></footer>'
    response += '</div></body></html>'
    return response



def generate_check_monthly_ui(groups):
    response = get_header('Returns a list of all users who didn\'t create a giveaway in a given month.','CheckMonthly')
    response += get_groups_dropdown(groups.values())
    response += get_year_month()

    response += get_optional_label()
    response += get_min_entries()
    response += get_min_days_with_game_stats()
    response += '<BR>'
    response += 'Minimum number of entries to ignore scores/review requirements: <input type="text" name="min_entries_override" size=3><BR><BR>'
    response += 'Ignore inactive users (users who did not enter any GA this month): <input type="checkbox" name="ignore_inactive_users" value="true"><BR>'
    response += get_footer('Get Monthly GAs')
    return response


def generate_user_check_rules_ui():
    response = get_header('Check if a user (not necessetily belonging to your group) complies to general rules (wins, level, etc.).', 'UserCheckRules')
    response += 'Warning: Please be patient, because it requires a connection to various external tools, this process may take some time.<BR><BR>'
    response += 'User: <input type="text" name="users"><BR><BR>'
    response += '<input type="checkbox" name="check_nonactivated" value="true">Check user doesn\'t have non activated games<BR>'
    response += '<input type="checkbox" name="check_multiple_wins" value="true">Check user doesn\'t have multiple wins<BR>'
    response += '<input type="checkbox" name="check_real_cv_value" value="true">Check user has positive real CV ratio<BR>'
    response += '<input type="checkbox" name="check_steamgifts_ratio" value="true">Check user has positive SteamGifts global ratio<BR>'
    response += '<input type="checkbox" name="check_steamrep" value="true">Check user has no SteamRep bans and his profile is public<BR>'
    response += '<input type="checkbox" name="check_level" value="true">Check user is above certain level. Level:  <input type="text" name="level" size=1>  <BR>'
    response += get_footer('Check User')
    return response


def generate_check_all_giveaways_ui(groups):
    response = get_header('Returns a list of games created not according to given rules.', 'CheckAllGiveawaysAccordingToRules')
    response += get_groups_dropdown(groups.values())

    response += get_optional_label()
    response += get_start_date()
    response += get_min_entries()
    response += get_min_days_with_game_stats()
    response += <BR>
    response += '<input type="checkbox" name="free_group_only" value="false">Check user did not create free group-only giveaways<BR>'

    response += get_footer('Check Giveaways')
    return response


def generate_user_check_first_giveaway_ui(groups):
    response = get_header('Check if users comply with first giveaway rules (according to defined rules).', 'UserCheckFirstGiveaway')
    response += get_groups_dropdown(groups.values())
    response += 'Users (comma-separated, e.g. Amy,Beck,Clark): <input type="text" name="users"><BR><BR>'
    response += 'User added to group on: <input type="date" name="addition_date" style="max-width: 200px;"><BR><BR>'

    response += get_optional_label()
    response += 'Within how many days of entering the group should the first GA be created: <input type="text" name="days_to_create_ga" size=2><BR><BR>'
    response += get_min_days('min_ga_time')
    response += get_min_entries()
    response += get_game_stats()
    response += get_footer('Check First Giveaway')
    return response


def generate_group_users_summary_ui(groups):
    response = get_header('For a given group, return summary of all giveaways created, entered and won by members.', 'GroupUsersSummary')
    response += get_groups_dropdown(groups.values())

    response += get_optional_label()
    response += get_start_date()
    response += get_footer('Get Users Summary')
    return response


def generate_user_full_giveaways_history_ui(groups):
    response = get_header('For a single user, show a detailed list of all giveaways he either created or participated in (Game link, value, score, winners, etc.).', 'UserFullGiveawaysHistory', '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>')

    response += get_groups_dropdown(groups.values())
    response += 'User:&nbsp; &nbsp;<select id="user" name="user">'
    response += '</select><BR><BR>'

    response += get_optional_label()
    response += get_start_date()
    response += get_footer('Get User History')

    response += '<script>'
    response += '$(\'#group_webpage\').on(\'change\', function() {'
    response += '$(\'#user\').html(\'\');'
    response += 'switch($(\'#group_webpage\').val()) {'
    for group in groups.values():
        response += 'case "' + group.group_webpage + '":'
        for user in sorted(group.group_users, key=lambda x: x.lower()):
          response += '$(\'#user\').append(\'<option value="' + user + '">' + user + '</option>\');'
        response += 'break;'
    response += '}});'
    response += '</script>'

    return response


def generate_lazy_add_group_ui():
    response = get_header('AddNewGroup - Add new group to SteamGifts Group Management Tool (SGMT).', 'AddNewGroup')
    response += 'In order to add your group to SGMT, you need to perform the following steps::<BR>' \
               '1. Add the SGMT user (<A HREF="http://steamcommunity.com/profiles/76561198811025715">Steam</A>, <A HREF="https://www.steamgifts.com/user/SGMT">SteamGifts</A>) to your group. This is a mock user approved by SteamGifts. You can check - it never enters any giveaways.<BR><BR>' \
               '2. Send a mail to <A HREF="mailto:sgmt.suport@gmail.com">sgmt.suport@gmail.com</A> with the name and link of the group you want to add.'\
               # '2. Add your group to the tool by using the button (and text box) below.<BR><BR>' \
               # 'Within 24 hours of the user appearing as member of your group in SteamGifts, and your group appearing under "processed" in the <A HREF="/SGMT/GetAvailableGroups">Groups page</A>. full abilities of the SGMT tool will be open to you.<BR><BR><BR>'
    # response += 'Group Webpage (SteamGifts): <input type="text" name="group_webpage" size=100><BR>'
    # response += get_footer('Add new group')
    return response


def generate_popular_giveaways_ui(groups):
    response = get_header('Get most popular giveaways in a group in a given month.', 'PopularGiveaways')
    response += get_groups_dropdown(groups.values())
    response += 'Measure popularity by:&nbsp; &nbsp;<select name="check_param">'
    response += '<option value="TotalEntries">Total number of entries in a GA</option>'
    response += '<option value="EntriesOnFinish">Number of entries on finished GAs</option>'
    response += '<option value="EntriesWithinXDays">Number of entries within X days of GA creation</option>'
    response += '</select>&nbsp; &nbsp;<BR><BR>'
    response += get_year_month()

    response += get_optional_label()
    response += '<input type="checkbox" name="group_only_users" value="true">Count only entries from users in the group<BR><BR>'
    response += 'If "Number of entries within X days of GA creation" was chosen, Number of days: <input type="text" name="num_of_days" size=3><BR><BR>'

    response += get_footer('Get popular giveaways')
    return response


def check_game_giveaways_ui(groups):
    response = get_header('Number of group entries every time a game was given away in the group.', 'CheckGameGiveaways')
    response += get_groups_dropdown(groups.values())
    response += 'Name of the Game: <input type="text" name="game_name"><BR><BR>'

    response += get_optional_label()
    response += get_start_date()
    response += get_footer('Get Giveaways Data')
    return response


def get_year_month():
    response = 'Year:&nbsp; &nbsp;<select name="year">'
    response += '<option value="2017">2017</option>'
    response += '<option value="2018">2018</option>'
    response += '<option value="2019">2019</option>'
    response += '<option value="2020">2020</option>'
    response += '<option value="2021">2021</option>'
    response += '<option value="2022">2022</option>'
    response += '<option value="2023">2023</option>'
    response += '<option value="2024">2024</option>'
    response += '<option value="2025">2025</option>'
    response += '</select>&nbsp; &nbsp;'

    response += 'Month:&nbsp; &nbsp;<select name="month">'
    for month in range(1, 13, 1):
        response += '<option value="' + str(month) + '">' + str(month) + '</option>'
    response += '</select><BR><BR>'

    return response


def get_min_entries():
    return 'Minimum number of entries: <input type="text" name="min_entries" size=2><BR><BR>'


def get_min_days_with_game_stats():
    response = get_min_days()
    response += get_game_stats()
    return response


def get_min_days(var_name='min_days'):
    return 'Minimum number of days of a GA to run: <input type="text" name="' + var_name + '" size=2><BR><BR>'


def get_game_stats():
    response = 'Minimal game value (in $) allowed: <input type="text" name="min_game_value" size=3><BR><BR>'
    response += 'Minimal number of Steam reviews allowed for a game: <input type="text" name="min_steam_num_of_reviews" size=6><BR><BR>'
    response += 'Minimal Steam score allowed for a game: <input type="text" name="min_steam_score" size=3><BR>'
    return response


def get_optional_label():
    return '<BR><B>Optional:</B><BR><BR>'


def get_start_date():
    return 'Start date: <input type="date" name="start_date" style="max-width: 200px;"><BR><BR>'



def get_groups_dropdown(groups):
    response = 'Group:&nbsp; &nbsp;<select id="group_webpage" name="group_webpage">'
    response += '<option/>'
    for group in groups:
        response += '<option value="' + group.group_webpage + '">' + group.group_name.replace('<', '&lt;') + '</option>'
    response += '</select><BR><BR>'
    return response

