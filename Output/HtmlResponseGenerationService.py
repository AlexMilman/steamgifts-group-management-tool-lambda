GLOBAL_STYLE = """
<style>
    body {
        font-family: 'Segoe UI', Roboto, Arial, sans-serif;
        background-color: #f9fafb;
        color: #1f2937;
        margin: 0;
        padding: 20px;
    }
    a {
        color: #2563eb;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    h2 {
        color: #111827;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 5px;
        margin-top: 30px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        background: #fff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-radius: 6px;
        overflow: hidden;
    }
    th, td {
        padding: 12px 16px;
        border-bottom: 1px solid #e5e7eb;
        text-align: left;
        font-size: 0.95em;
    }
    th {
        background-color: #f1f5f9;
        font-weight: 600;
    }
    tr:hover {
        background-color: #f9fafb;
    }
    .highlight {
        background-color: #e0f2fe;
    }
    .winner {
        font-weight: bold;
        color: #10b981;
    }
    .section {
        margin-bottom: 40px;
    }
</style>
"""

# HTML response generation service of SGMT
# Copyright (C) 2017  Alex Milman
import calendar
from datetime import datetime

from BusinessLogic.ScrapingUtils import SteamGiftsConsts, SGToolsConsts, SteamConsts, SteamRepConsts


def generate_invalid_giveaways_response(games, invalid_giveaways, free_games):
    response = GLOBAL_STYLE + '\n'
    if not invalid_giveaways and not free_games:
        response += u'<B>No Invalid Giveaways or Free Games found !</B>'

    if invalid_giveaways:
        response += u'<B>Invalid Giveaways:</B>'
        for user, user_giveaways in invalid_giveaways.items():
            response += u'<BR>User ' + generate_user_link(user) + ':<BR>'

            for giveaway in sorted(user_giveaways, key=lambda x: x.end_time or datetime.datetime.min, reverse=True):
                game_name = giveaway.game_name
                game_data = games[game_name]
                response += u'<A HREF="' + giveaway.link + u'">' + game_name + u'</A>'
                if game_data:
                    response += u' (Steam Value: ' + str(game_data.value) + u', Steam Score: ' + str(
                        game_data.steam_score) + u', Num Of Reviews: ' + str(game_data.num_of_reviews) + u')'
                response += u' Ends on: ' + giveaway.end_time.strftime('%Y-%m-%d %H:%M:%S')
                response += u'<BR>'
        response += u'<BR><BR>'

    if free_games:
        response += u'<B>Games given away for free (marked as ** on SteamGifts):</B>'
        for user, user_giveaways in free_games.items():
            response += u'<BR>User ' + generate_user_link(user) + ':<BR>'

            for giveaway in sorted(user_giveaways, key=lambda x: x.end_time, reverse=True):
                game_name = giveaway.game_name
                game_data = games[game_name]
                response += u'<A HREF="' + giveaway.link + u'">' + game_name + u'</A>'
                if game_data:
                    response += u' (Steam Value: ' + str(game_data.value) + u', Steam Score: ' + str(
                        game_data.steam_score) + u', Num Of Reviews: ' + str(game_data.num_of_reviews) + u')'
                response += u' Ends on: ' + giveaway.end_time.strftime('%Y-%m-%d %H:%M:%S')
                response += u'<BR>'

    return response


def generate_user_full_history_response(created_giveaways, entered_giveaways, games, user):
    response = GLOBAL_STYLE + '\n'
    response += u'<BR>User ' + generate_user_link(user) + ':<BR>'
    total_value = 0
    total_score = 0.0
    total_num_of_reviews = 0.0
    missing_data = 0
    for giveaway in created_giveaways:
        game_data = games[giveaway.game_name]
        if game_data:
            total_value += game_data.value
            total_score += game_data.steam_score
            total_num_of_reviews += game_data.num_of_reviews
        if not game_data or (game_data.steam_score == -1 and game_data.num_of_reviews == -1):
            missing_data += 1
    response += u'<BR>User created ' + str(len(created_giveaways)) + u' giveaways '
    if len(created_giveaways) > 1:
        total = len(created_giveaways) - missing_data
        response += u'(Total value of given away games: $' + str(total_value)
        if total > 0:
            response += u' Average game score: ' + str(total_score / total) + u' Average Num of reviews: ' + str(
                total_num_of_reviews / total)
        response += ')'
    response += u'<BR>'
    for giveaway in sorted(created_giveaways, key=lambda x: x.end_time, reverse=True):
        game_name = giveaway.game_name
        game_data = games[game_name]
        response += u'<A HREF="' + giveaway.link + u'">' + game_name + u'</A>'
        if game_data:
            response += u' (Steam Value: ' + str(game_data.value) + u', Steam Score: ' + str(
                game_data.steam_score) + u', Num Of Reviews: ' + str(game_data.num_of_reviews) + u')'
        response += u' Number of entries: ' + str(len(giveaway.entries)) + ', '
        if giveaway.end_time > datetime.now():
            response += u' Ends on: '
        else:
            response += u' Ended on: '
        response += giveaway.end_time.strftime('%Y-%m-%d %H:%M:%S')
        response += u'<BR>'
    won = 0
    for giveaway in entered_giveaways:
        if user in giveaway.entries.keys() and giveaway.entries[user].winner:
            won += 1
    response += u'<BR>User entered ' + str(len(entered_giveaways)) + u' giveaways:<BR>'
    if won > 0:
        response = response[:-4]
        response += u' (Won ' + str(won) + u', Winning percentage: ' + str(
            float(won) / len(entered_giveaways) * 100) + u'%)<BR>'
    for giveaway in sorted(entered_giveaways, key=lambda x: x.end_time, reverse=True):
        game_data = games[giveaway.game_name]
        response += u'<A HREF="' + giveaway.link + u'">' + giveaway.game_name + u'</A>'
        if game_data:
            response += u' (Steam Value: ' + str(game_data.value) + u', Steam Score: ' + str(
                game_data.steam_score) + u', Num Of Reviews: ' + str(game_data.num_of_reviews) + u')'
        response += u', Ends on: ' + giveaway.end_time.strftime('%Y-%m-%d %H:%M:%S')
        if giveaway.entries[user].entry_time:
            response += u', Entry date: ' + giveaway.entries[user].entry_time.strftime('%Y-%m-%d %H:%M:%S')
        if user in giveaway.entries.keys() and giveaway.entries[user].winner:
            response += u' <B>(WINNER)</B>'
        response += u'<BR>'
    return response


def generate_group_users_summary_response(group_webpage, total_group_data, users_data, start_date):
    response = GLOBAL_STYLE + '\n'
    response += u'Summary for group ' + group_webpage + u':<BR><BR>'
    # Total Giveaways Count, Total Games Value, Average games value, Average Game Score, Average Game NumOfReviews, Average number of entered per game, Average number of created per user, Average number of entrered per user, Average number of won per user
    response += u'Total number of giveaway: ' + float_to_str(total_group_data[0]) + u'<BR><BR>'
    response += u'Total value of games given away in group: $' + float_to_str(total_group_data[1]) + u'<BR>'
    response += u'Total number of users: ' + str(len(users_data)) + u'<BR>'

    response += u'Average value of a game: $' + float_to_str(total_group_data[2]) + u'<BR>'
    response += u'Average steam score per game: ' + float_to_str(total_group_data[3]) + u'<BR>'
    response += u'Average number of steam reviews per game: ' + float_to_str(total_group_data[4]) + u'<BR>'
    response += u'Average number of group member entries per giveaway: ' + float_to_str(
        total_group_data[5]) + u'<BR><BR>'

    response += u'Average number of giveaways created by user: ' + float_to_str(total_group_data[6]) + u'<BR>'
    response += u'Average number of giveaways entered by user: ' + float_to_str(total_group_data[7]) + u'<BR>'
    response += u'Average number of giveaways won by user: ' + float_to_str(total_group_data[8]) + u'<BR>'
    response += u'<BR><BR>Summaries for all group users:<BR>'
    for user_name in sorted(users_data.keys(), key=lambda x: users_data[x][1], reverse=True):
        user_data = users_data[user_name]
        response += u'<BR>User ' + generate_full_data_link(group_webpage, start_date, user_name) + ':<BR>'
        # Number of created GAs, Total Value, Average Value, Average Score, Average NumOfReviews
        user_created = user_data[0]
        if user_created:
            response += u'Created: '
            response += u'Number of GAs: ' + float_to_str(user_created[0]) \
                        + u', Total GAs value: $' + float_to_str(user_created[1]) \
                        + u', Average GA value: $' + float_to_str(user_created[2]) \
                        + u', Average GA Steam game score: ' + float_to_str(user_created[3]) \
                        + u', Average GA Steam number of reviews: ' + float_to_str(user_created[4]) + u'<BR>'

        # Number of entered GAs, Percentage of unique, Total Value, Average Value, Average Score, Average Num Of Reviews
        user_entered = user_data[1]
        if user_entered:
            response += u'Entered: '
            response += u'Number of GAs: ' + float_to_str(user_entered[0]) \
                        + u', Probability of winning: ' + float_to_str(user_entered[1]) + u'%' \
                        + u', Group-only GAs: ' + float_to_str(user_entered[2]) + u'%' \
                        + u', Total GAs value: $' + float_to_str(user_entered[3]) \
                        + u', Average GA value: $' + float_to_str(user_entered[4]) \
                        + u', Average GA Steam game score: ' + float_to_str(user_entered[5]) \
                        + u', Average GA Steam number of reviews: ' + float_to_str(user_entered[6]) + u'<BR>'

        # Number of won GAs, Winning percentage, Total value, Average Value, Average Score, Average Num Of Reviews
        user_won = user_data[2]
        if user_won:
            response += u'Won: '
            response += u'Number of GAs: ' + float_to_str(user_won[0]) \
                        + u', Won vs total entered: ' + float_to_str(user_won[1]) + u'%' \
                        + u', Total GAs value: $' + float_to_str(user_won[2]) \
                        + u', Average GA value: $' + float_to_str(user_won[3]) \
                        + u', Average GA Steam game score: ' + float_to_str(user_won[4]) \
                        + u', Average GA Steam number of reviews: ' + float_to_str(user_won[5]) + u'<BR>'

        if user_created and user_won:
            response += u'Created/Won ratio: '
            response += u'Number of GAs ratio: ' + float_to_str(float(user_created[0]) / user_won[0]) \
                        + u', GAs value ratio: ' + float_to_str(user_created[1] / user_won[2]) + u'<BR>'

    return response


def generate_check_monthly_response(group_webpage, users, monthly_posters, monthly_unfinished, inactive_users,
                                    cakeday_users, year_month):
    response = GLOBAL_STYLE + '\n'
    response += u'<BR><B>' + get_month_year_str(year_month) + u'</B><BR>'

    response += u'<BR>Users with unfinished monthly GAs:<BR>'
    for user, giveaways in monthly_unfinished.items():
        if user not in monthly_posters:
            response += u'User ' + generate_user_link(user) + u' giveaways: '
            if giveaways and len(giveaways) > 0:
                for giveaway in giveaways:
                    response += u'<A HREF="' + giveaway.link + u'">' + giveaway.game_name + u'</A>, '
                response = response[:-2]
                response += '<BR>'

    if inactive_users:
        response += u'<BR><BR>Users inactive this month (did not enter any GAs):<BR>'
        for user in inactive_users:
            response += generate_full_data_link(group_webpage, '', user) + u'<BR>'

    if cakeday_users:
        response += u'<BR><BR>Users with a cakeday this month (don\'t need to create a monthly giveaway):<BR>'
        for user in cakeday_users:
            response += generate_user_link(str(user)) + u'<BR>'

    response += u'<BR><BR>Users without monthly giveaways:<BR>'
    response += u'<TABLE style="width:35%">'
    for user, user_data in users.items():
        if user not in monthly_posters and user not in monthly_unfinished.keys() and (
                not inactive_users or user not in inactive_users) and (not cakeday_users or user not in cakeday_users):
            response += u'<TR>'
            response += u'<TH>' + generate_user_link(str(user)) + u'</TH><TH>' + generate_full_data_link(group_webpage,
                                                                                                         '', user,
                                                                                                         'User full GAs list') + u'</TH><TH>' + generate_steam_user_link(
                user_data.steam_id, user_data.steam_user_name) + u'</TH>'
            response += u'</TR>'
    response += u'</TABLE>'

    return response


def generate_check_user_first_giveaway_response(user_first_giveaway, succesfully_ended, user_no_giveaway,
                                                user_entered_giveaway, time_to_create_over):
    response = GLOBAL_STYLE + '\n'
    for user_name in user_first_giveaway.keys():
        for group_giveaway, game_data in user_first_giveaway[user_name]:
            response += u'User ' + generate_user_link(user_name) + ' ' \
                                                                   u'first giveaway: <A HREF="' + group_giveaway.link + u'">' + group_giveaway.game_name + u'</A> ' \
                                                                                                                                                           u' (Steam Value: ' + str(
                game_data.value) + u', Steam Score: ' + str(game_data.steam_score) + u', Num Of Reviews: ' + str(
                game_data.num_of_reviews) + u')'
            if user_name in succesfully_ended and group_giveaway.link in succesfully_ended[user_name]:
                response += u'<B> - Finished succesfully !!!</B>'
            elif datetime.now() <= group_giveaway.end_time:
                response += u' - Ends on: ' + group_giveaway.end_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                response += u' - Ended'
            response += u'<BR>'

    response += u'<BR>'
    for user in user_no_giveaway:
        response += u'User ' + generate_user_link(user) + ' did not create a GA yet!<BR>'

    response += u'<BR>'
    for user in user_entered_giveaway:
        group_giveaways = user_entered_giveaway[user]
        for group_giveaway in sorted(group_giveaways, key=lambda x: x.entries[user].entry_time, reverse=True):
            response += u'User ' + generate_user_link(user) + ' ' \
                                                              u'entered giveaway before his first giveaway was over: <A HREF="' + group_giveaway.link + '">' + group_giveaway.game_name + u'</A> ' \
                                                                                                                                                                                          u'(Entry date: ' + \
                        group_giveaway.entries[user].entry_time.strftime('%Y-%m-%d %H:%M:%S') + u')<BR>'

    if time_to_create_over:
        response += u'<BR>Time to create first GA ended.<BR>'

    return response


def generate_user_check_rules_response(user, check_nonactivated, check_multiple_wins, check_real_cv_ratio,
                                       check_steamgifts_ratio, check_level, check_steamrep):
    response = GLOBAL_STYLE + '\n'
    response += u'<BR>User <B>' + user + u':</B><BR>'
    if check_nonactivated:
        response += u'Check non-activated games: ' + linkify(
            SGToolsConsts.SGTOOLS_CHECK_NONACTIVATED_LINK + user) + u'<BR><BR>'

    if check_multiple_wins:
        response += u'Check multiple wins: ' + linkify(
            SGToolsConsts.SGTOOLS_CHECK_MULTIPLE_WINS_LINK + user) + u'<BR><BR>'

    if check_steamgifts_ratio or check_real_cv_ratio or check_level:
        response += u'Check won/sent ratio & level on SteamGifts: ' + linkify(
            SteamGiftsConsts.get_user_link(user)) + '<BR><BR>'

    if check_steamrep is not None:
        response += u'Get user ID from SteamGifts: ' + linkify(SteamGiftsConsts.get_user_link(user)) + u' ()<BR>'
        response += u'Check user is not public or banned: ' + linkify(
            SteamRepConsts.STEAMREP_CHECK_PROFILE) + u' + id ()<BR>'

    return response


def generate_popular_giveaways_response(popular_giveaways, year_month):
    response = GLOBAL_STYLE + '\n'
    response += u'<BR><B>Most Popular GAs for ' + get_month_year_str(year_month) + u':</B><BR><BR>'
    response += u'<TABLE style="width:45%">'
    for giveaway_data, num_of_entries in sorted(popular_giveaways.items(), key=lambda item: item[1], reverse=True):
        response += u'<TR>'
        response += u'<TH><A HREF="' + giveaway_data.link + u'">' + giveaway_data.game_name + u' </A></TH><TH>By: ' + generate_user_link(
            giveaway_data.creator) + '</TH><TH>Entries: ' + str(num_of_entries) + u'</TH>'
        response += u'</TR>'
    response += u'</TABLE>'

    return response


def generate_all_game_giveaways_response(game_name, all_game_giveaways):
    response = GLOBAL_STYLE + '\n'
    response += u'<BR><B>Full list of "' + game_name + u'" GAs:</B><BR><BR>'
    response += u'<TABLE style="width:75%">'
    response += u'<B><TH>Game Name</TH><TH>Gifter</TH><TH>Group Entries</TH><TH>Start Time</TH><TH>End Time</TH></B>'
    for giveaway_data, num_of_entries in sorted(all_game_giveaways.items(), key=lambda item: item[0].end_time,
                                                reverse=True):
        response += u'<TR>'
        response += u'<TH><A HREF="' + giveaway_data.link + u'">' + giveaway_data.game_name + u' </A></TH><TH>' + generate_user_link(
            giveaway_data.creator) + '</TH><TH>' + str(num_of_entries) + u'</TH><TH>' + str(
            giveaway_data.start_time) + u'</TH><TH>' + str(giveaway_data.end_time) + u'</TH>'
        response += u'</TR>'
    response += u'</TABLE>'

    return response


def get_month_year_str(year_month):
    split_date = year_month.split('-')
    year = split_date[0]
    month = calendar.month_name[int(split_date[1])]
    month_year_str = month + u' ' + year
    return month_year_str


def linkify(url):
    return u'<A HREF="' + url + '">' + url + '</A>'


def generate_user_link(user):
    return u'<A HREF="' + SteamGiftsConsts.get_user_link(user) + u'">' + user + u'</A>'


def generate_steam_user_link(steam_id, steam_user_name):
    if not steam_user_name:
        steam_user_name = ''
    return u'<A HREF=' + SteamConsts.STEAM_PROFILE_LINK + steam_id + '>Steam (' + steam_user_name + ')</A>'


def generate_full_data_link(group_webpage, start_date, user_name, label=None):
    if not label:
        label = user_name
    return u'<A HREF="/SGMT/UserFullGiveawaysHistory?group_webpage=' + group_webpage + u'&user=' + user_name + u'&start_date=' + start_date + u'">' + label + u'</A>'


def generate_get_groups_response(empty_groups, groups):
    response = GLOBAL_STYLE + '\n'
    response += u'<B>Available Groups:</B><BR>'
    for group_name in groups.keys():
        if group_name not in empty_groups.keys():
            response += u'<BR> - <A HREF="' + groups[group_name] + '">' + group_name.replace('<', '&lt;') + u'</A><BR>'

    response += u'<BR><BR>'
    response += u'<B>Groups awaiting processing:</B><BR>'
    for group_name in empty_groups.keys():
        response += u'<BR> - <A HREF="' + empty_groups[group_name] + u'">' + group_name.replace('<',
                                                                                                '&lt;') + u'</A><BR>'
    return response


def float_to_str(float_value):
    float_str = str(float_value)
    if '.' in float_str:
        float_split = float_str.split('.')
        if float_split[1] == '0':
            return float_split[0]
        after_decimal_point = len(float_split[1])
        if after_decimal_point > 2:
            return float_str[:-after_decimal_point + 2]
    return float_str


