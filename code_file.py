import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import io
import base64

class TelegramAnalytics:
    def __init__(self, data_path=None):
        """
        Initialize analytics with optional data source
        """
        # Ensure non-interactive backend
        plt.switch_backend('Agg')
        self.generate_sample_data()

    def generate_sample_data(self):
        """
        Generate sample datasets for demonstration
        """
        np.random.seed(42)
        start_date = datetime.now() - timedelta(days=30)
        
        # Sample Group Data
        self.groups = pd.DataFrame({
            'group_id': range(1, 11),
            'title': [f'Group {i}' for i in range(1, 11)],
            'group_type': np.random.choice(['public', 'private'], 10),
            'member_count': np.random.randint(50, 500, 10)
        })

        # Sample Member Data
        self.members = pd.DataFrame({
            'user_id': range(1, 101),
            'username': [f'user_{i}' for i in range(1, 101)],
            'is_bot': np.random.choice([True, False], 100, p=[0.1, 0.9]),
            'group_id': np.random.randint(1, 11, 100)
        })

        # Sample Message Data
        self.messages = pd.DataFrame({
            'message_id': range(1, 1001),
            'sender_id': np.random.randint(1, 101, 1000),
            'group_id': np.random.randint(1, 11, 1000),
            'timestamp': [start_date + timedelta(hours=i) for i in range(1000)],
            'message_type': np.random.choice(['text', 'media', 'link'], 1000),
            'replies': np.random.randint(0, 10, 1000),
            'views': np.random.randint(10, 100, 1000)
        })

    def _generate_plot(self, plot_func):
        """
        Generate a base64 encoded plot
        """
        plt.clf()  # Clear any existing plots
        fig, ax = plt.subplots(figsize=(10, 6))
        plot_func(ax)
        
        # Save to a bytes buffer
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        
        # Encode to base64
        return base64.b64encode(buf.getvalue()).decode('utf-8')

    def daily_messages_sent(self):
        """
        Tracks number of messages sent daily in each group
        """
        # Group by date and group_id, count messages
        daily_messages = self.messages.groupby([
            pd.Grouper(key='timestamp', freq='D'), 
            'group_id'
        ]).size().unstack(fill_value=0)
        
        # Convert index to string for JSON serialization
        daily_messages.index = daily_messages.index.strftime('%Y-%m-%d')
        
        # Generate plot
        def plot_daily_messages(ax):
            daily_messages.plot(kind='bar', stacked=True, ax=ax)
            ax.set_title('Daily Messages Sent per Group')
            ax.set_xlabel('Date')
            ax.set_ylabel('Number of Messages')
            ax.tick_params(axis='x', rotation=45)
        
        # Generate base64 encoded plot
        plot_base64 = self._generate_plot(plot_daily_messages)
        
        # Return a dictionary that can be easily serialized
        return {
            'data': daily_messages.to_dict(),
            'groups': list(daily_messages.columns),
            'plot': plot_base64
        }

    def most_active_members(self, top_n=10):
        """
        Identifies members who send the most messages
        """
        # Count messages per member
        member_message_count = self.messages['sender_id'].value_counts().head(top_n)
        
        # Generate plot
        def plot_active_members(ax):
            member_message_count.plot(kind='bar', ax=ax)
            ax.set_title(f'Top {top_n} Most Active Members')
            ax.set_xlabel('User ID')
            ax.set_ylabel('Number of Messages')
        
        # Generate base64 encoded plot
        plot_base64 = self._generate_plot(plot_active_members)
        
        # Return dictionary for JSON serialization
        return {
            'data': member_message_count.to_dict(),
            'users': list(member_message_count.index),
            'plot': plot_base64
        }

    def group_growth_rate(self):
        """
        Monitors rate of new members joining groups
        """
        # Count members per group
        group_growth = self.members.groupby('group_id').size()
        
        # Generate plot
        def plot_group_growth(ax):
            group_growth.plot(kind='bar', ax=ax)
            ax.set_title('Group Membership Size')
            ax.set_xlabel('Group ID')
            ax.set_ylabel('Number of Members')
        
        # Generate base64 encoded plot
        plot_base64 = self._generate_plot(plot_group_growth)
        
        # Return dictionary for JSON serialization
        return {
            'data': group_growth.to_dict(),
            'groups': list(group_growth.index),
            'plot': plot_base64
        }

# Example usage
if __name__ == '__main__':
    analytics = TelegramAnalytics()
    print(analytics.daily_messages_sent())
    print(analytics.most_active_members())
    print(analytics.group_growth_rate())